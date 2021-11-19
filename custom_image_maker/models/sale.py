# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from itertools import groupby


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    solid = fields.Boolean('BEST ESTIMATE')
    srv_start_date = fields.Date('Fecha estimada de inicio')
    srv_end_date = fields.Date('Fecha fin de servicios')
    percentage = fields.Float("Porcentaje")
    validate = fields.Boolean('Validar', default=False)
    validate_readonly = fields.Boolean('Validar', compute='_compute_validate_readonly')
    discount_validate = fields.Boolean('Validar Desc.', compute="_compute_discount_validate", store=True)
    lock = fields.Boolean(string='Lock', compute="_compute_lock_validate")
    higher_discount = fields.Float('Higher', compute="_compute_discount_validate", store=True)
    estado = fields.Selection(selection=[
        ('solid', 'Solid'),
        ('stretch', 'Stretch'),
        ('best', 'Best Case'),
        ('lost', 'No ganado')
    ])
    periodo = fields.Float('Período')
    imteam_id = fields.Many2one('sale.imteam', string='Equipo')
    product_id = fields.Many2one('product.product', string='Servicio', required=True, ondelete='restrict',
                                 domain="[('type', '=', 'service')]")

    def _compute_validate_readonly(self):
        for record in self:
            readonly = True
            if record.user_has_groups('custom_image_maker.group_im_validation'):
                readonly = False
            record.validate_readonly = readonly


    def _compute_lock_validate(self):
        for rec in self:
            lock = True
            amount_user = self.env.user.approve_discount
            if amount_user:
                if rec.higher_discount <= amount_user:
                    lock = False
            rec.lock = lock

    @api.depends('order_line')
    def _compute_discount_validate(self):
        for rec in self:
            discount_validate = False
            higher = 0.0
            amount_company = self.env.company.discount_level
            if rec.order_line:
                line_discount = rec.order_line.mapped('discount')
                line_discount.sort(reverse=True)
                if line_discount:
                    higher = line_discount[0]
                    if higher > amount_company:
                        discount_validate = True
            rec.higher_discount = higher
            rec.validate = False
            rec.discount_validate = discount_validate

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.
        invoice_vals_list = []
        invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines(final)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, order._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                if invoice_item_sequence == 0:
                    invoice_line_vals.append(
                        (0, 0, line._prepare_one_service_invoice_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                else:
                    invoice_line_vals[0][2]['quantity'] = 1
                    invoice_line_vals[0][2]['price_unit'] += line.price_unit
                invoice_item_sequence += 1

            if self.currency_id.name == 'UF':
                if self.currency_id.rate > 0:
                    rate = 1 / self.currency_id.rate
                    invoice_line_vals[0][2]['price_unit'] = invoice_line_vals[0][2]['price_unit'] * rate

            invoice_line_vals[0][2]['name'] = self.product_id.name
            invoice_line_vals[0][2]['product_id'] = self.product_id.id

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise self._nothing_to_invoice_error()

        # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys])
            for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                origins = set()
                payment_refs = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    payment_refs.add(invoice_vals['payment_reference'])
                    refs.add(invoice_vals['ref'])
                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins),
                    'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.

        # As part of the invoice creation, we make sure the sequence of multiple SO do not interfere
        # in a single invoice. Example:
        # SO 1:
        # - Section A (sequence: 10)
        # - Product A (sequence: 11)
        # SO 2:
        # - Section B (sequence: 10)
        # - Product B (sequence: 11)
        #
        # If SO 1 & 2 are grouped in the same invoice, the result will be:
        # - Section A (sequence: 10)
        # - Section B (sequence: 10)
        # - Product A (sequence: 11)
        # - Product B (sequence: 11)
        #
        # Resequencing should be safe, however we resequence only if there are less invoices than
        # orders, meaning a grouping might have been done. This could also mean that only a part
        # of the selected SO are invoiceable, but resequencing in this case shouldn't be an issue.
        if len(invoice_vals_list) < len(self):
            SaleOrderLine = self.env['sale.order.line']
            for invoice in invoice_vals_list:
                sequence = 1
                for line in invoice['invoice_line_ids']:
                    line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                    sequence += 1

        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        if final:
            moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
        for move in moves:
            move.message_post_with_view('mail.message_origin_link',
                values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                subtype_id=self.env.ref('mail.mt_note').id
            )
        return moves

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_order_template_id = fields.Many2one('sale.order.template', related='order_id.sale_order_template_id', readonly=False)
    is_a_project = fields.Boolean(related='product_id.is_a_project')

    @api.onchange('sale_order_template_id')
    def onchange_sale_template_id(self):
        if self.sale_order_template_id:
            if self.sale_order_template_id.is_project:
                products = self.env['product.product'].search([('sale_ok', '=', True,),('company_id','=',False),('is_a_project', '=', True)])
            else:
                products = self.env['product.product'].search([('sale_ok', '=', True,), ('company_id', '=', False)])
            return {'domain': {'product_id': [('id', 'in', products.ids)]}}

    def _prepare_one_service_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res


class SaleTeam(models.Model):
    _name = 'sale.imteam'
    _description = 'Equipo de trabajo'

    name = fields.Char('Nombre')
    # order_id = fields.Many2one('Sale Order')
