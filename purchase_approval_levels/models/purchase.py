# coding: utf-8
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('director', 'Para aprobar por Director')])

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        approval_levels = self.env.company.po_double_validation
        if approval_levels == 'two_step':
            return self.user_has_groups('purchase_approval_levels.group_purchase_director')
        else:
            return super(PurchaseOrder, self)._approval_allowed()

    def button_confirm(self):
        approval_levels = self.env.company.po_double_validation
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if approval_levels == 'two_step':
                if order.amount_total <= self.env.company.currency_id._convert(order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()):
                    if order._approval_allowed():
                        order.button_approve()
                    elif order.user_has_groups('purchase.group_purchase_manager') or order.user_has_groups('purchase_approval_levels.group_purchase_boss'):
                        order.write({'state': 'director'})
                    else:
                        order.write({'state': 'to approve'})
                    if order.partner_id not in order.message_partner_ids:
                        order.message_subscribe([order.partner_id.id])
                else:
                    if order._approval_allowed():
                        order.button_approve()
                    elif order.user_has_groups('purchase_approval_levels.group_purchase_boss'):
                        order.write({'state': 'director'})
                    else:
                        order.write({'state': 'to approve'})
                    if order.partner_id not in order.message_partner_ids:
                        order.message_subscribe([order.partner_id.id])
        return True

    def button_approve_boss(self):
        approval_levels = self.env.company.po_double_validation
        directors = self.env['res.users'].search([('id', 'in', self.env.ref('purchase_approval_levels.group_purchase_director').users.ids)])
        boss1 = self.env['res.users'].search([('id', 'in', self.env.ref('purchase.group_purchase_manager').users.ids)])
        boss2 = self.env['res.users'].search([('id', 'in', self.env.ref('purchase_approval_levels.group_purchase_boss').users.ids)])
        for order in self:
            if approval_levels == 'two_step':
                if order.amount_total <= self.env.company.currency_id._convert(order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()):
                    if order._approval_allowed():
                        order.button_approve()
                    elif order.user_has_groups('purchase_approval_levels.group_purchase_boss') or order.user_has_groups('purchase.group_purchase_manager'):
                        order.write({'state': 'director'})
                    else:
                        users = ''
                        user_list = []
                        for director in directors:
                            user_list.append(director.name)
                        for b2 in boss2:
                            user_list.append(b2.name)
                        for b1 in boss1:
                            user_list.append(b1.name)
                        user_list = set(user_list)
                        for user in user_list:
                            users += user + '\n'
                        raise ValidationError('La compra solo puede ser aprobada por: \n%s' % users)
                else:
                    if order._approval_allowed():
                        order.button_approve()
                    elif order.user_has_groups('purchase_approval_levels.group_purchase_boss'):
                        order.write({'state': 'director'})
                    else:
                        users = ''
                        user_list = []
                        for director in directors:
                            user_list.append(director.name)
                        for b2 in boss2:
                            user_list.append(b2.name)
                        user_list = set(user_list)
                        for user in user_list:
                            users += user + '\n'
                        raise ValidationError('La compra solo puede ser aprobada por: \n%s' % users)

    def button_approve(self, force=False):
        approval_levels = self.env.company.po_double_validation
        if approval_levels == 'two_step':
            directors = self.env['res.users'].search([('id', 'in', self.env.ref('purchase_approval_levels.group_purchase_director').users.ids)])
            if self._approval_allowed():
                self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
                self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
                return {}
            else:
                users = ''
                user_list = []
                for director in directors:
                    user_list.append(director.name)
                user_list = set(user_list)
                for user in user_list:
                    users += user + '\n'
                raise ValidationError('La compra solo puede ser aprobada por: \n%s' % users)
        else:
            return super(PurchaseOrder, self).button_approve()