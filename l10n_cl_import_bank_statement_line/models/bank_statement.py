# -*- coding: utf-8 -*-
# Part of Konos. See LICENSE file for full copyright and licensing details.

import tempfile
import binascii
import logging
import io
from datetime import date
from datetime import datetime
from odoo.exceptions import Warning
from odoo import models, fields, api, exceptions, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

_logger = logging.getLogger(__name__)
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class account_bank_statement_wizard(models.TransientModel):
    _name = "account.bank.statement.wizard"

    file = fields.Binary('File')
    file_opt = fields.Selection([('excel', 'Excel'), ('csv', 'CSV')], default='excel')
    bank_opt = fields.Selection(
        [('santander', 'Santander'), ('estado', 'Banco Estado'), ('chile', 'Banco de Chile'), 
        ('itau', 'Banco Itau'), ('tdci', 'TC Internacional Banco Chile'), ('tdcn', 'TC Nacional Banco Chile'), 
        ('bice', 'Banco Bice'), ('bci', 'BCI'), ('scotiabank', 'Scotia Bank'), ('security', 'Banco Security')])

    #@api.model
    def import_file(self):  # Fecha actual
        res = False
        now = datetime.now()
        years = now.year
        active_id = (self._context.get('active_id'))
        bank_statement = self.env['account.bank.statement'].browse(active_id)
        # if not file:
        #    raise Warning('Please Select File')
        if self.file_opt == 'csv':
            keys = ['date', 'ref', 'partner', 'memo', 'amount']
            data = base64.b64decode(self.file)
            file_input = io.StringIO(data.decode("utf-8"))
            file_input.seek(0)
            reader_info = []
            reader = csv.reader(file_input, delimiter=',')

            try:
                reader_info.extend(reader)
            except Exception:
                raise exceptions.Warning(_("Not a valid file!"))
            values = {}
            for i in range(len(reader_info)):
                field = list(map(str, reader_info[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        res = self._create_statement_lines(values)
        elif self.file_opt == 'excel':
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            contador = 0
            if self.bank_opt == 'santander':
                contador = 16
                header = {}
                values_header = [sheet.cell_value(15, i) for i in range(sheet.ncols)]
                for row_no in range(16, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if header['MONTO'] == 'Resumen comisiones':
                        break
                    if header['MONTO'] == 'Saldos diarios':
                         break
                    values['statement_id'] = active_id
                    values['amount'] = header['MONTO']
                    values['date'] = datetime.strptime(
                        header['FECHA'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['DESCRIPCIÓN MOVIMIENTO']
                    values['narration'] = header['CARGO/ABONO']

                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'chile':
                contador = 22
                header = {}
                values_header = [sheet.cell_value(21, i) for i in range(sheet.ncols)]
                for row_no in range(22, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if header['Fecha'] == 'Saldo (CLP)':
                        break
                    values['statement_id'] = active_id
                    amount = header['Abonos (CLP)'] or header['Cargos (CLP)']
                    values['amount'] = amount
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'security':
                contador = 14
                header = {}
                values_header = [sheet.cell_value(13, i) for i in range(sheet.ncols)]
                for row_no in range(14, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if not(header['fecha ']):
                        break
                    values['statement_id'] = active_id
                    excel_date = header['fecha ']
                    convert_date = datetime(*xlrd.xldate_as_tuple(excel_date, 0))
                    values['date'] = convert_date.strftime('%Y-%m-%d')
                    values['amount'] = header['cargos '] or header['abonos ']
                    values['payment_ref'] = header['descripción ']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'tdcn':
                contador = 19
                header = {}
                values_header = [sheet.cell_value(18, i) for i in range(sheet.ncols)]
                for row_no in range(19, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    
                    if not header['Fecha']:
                        break
                    values['statement_id'] = active_id
                    values['amount'] = header['Montos'] * (-1)
                    #values['amount'] = header['Abonos (CLP)']
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    # vals['amount'] = values_es['MONTO']
                    #values['narration'] = header['CARGO/ABONO']

                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'tdci':
                contador = 19
                header = {}
                values_header = [sheet.cell_value(18, i) for i in range(sheet.ncols)]
                for row_no in range(19, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    # line = list(
                    #     map(lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value),
                    #         sheet.row(row_no)))
                    # logging.info(line[0])
                    # logging.info(type(line[0]))
                    # try:
                    #     fecha = line[3].decode("utf-8")
                    #     date_string = datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
                    #     print(date_string)
                    #     values.update({'date': date_string,
                    #                    'ref': '',
                    #                    'partner': line[7],
                    #                    'memo': line[1].decode("utf-8"),
                    #                    'amount': float(line[0]),
                    #                    })
                    #     #res = self._create_statement_lines(values)
                    #     bank_statement.write([0, 0, values])
                    # except Exception as e:
                    #     _logger.warning(str(e))
                    if not header['Fecha']:
                        break
                    values['statement_id'] = active_id
                    values['amount'] = header['Monto'] * (-1)
                    #values['amount'] = header['Abonos (CLP)']
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    # vals['amount'] = values_es['MONTO']
                    #values['narration'] = header['CARGO/ABONO']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'bice':
                contador = 10
                header = {}
                years_format = str(years)
                values_header = [sheet.cell_value(9, i) for i in range(sheet.ncols)]
                for row_no in range(10, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if not header['Fecha']:
                        break                    
                    values['statement_id'] = active_id
                    if header['Fecha'] == '  -  ':
                        header['Fecha'] = ''
                    else:
                        a = datetime.strptime(header['Fecha'] + '-' + years_format, '%d-%m-%Y').strftime('%Y-%m-%d')
                        values['date'] = a
                    values['payment_ref'] = header['Descripción']
                    values['amount'] = header['Cargos'] if header['Cargos'] else header['Abonos']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'bci':
                contador = 2
                header = {}
                values_header = [sheet.cell_value(1, i) for i in range(sheet.ncols)]
                for row_no in range(2, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if not header['Fecha']:
                        break
                    abono = header['Abono $']
                    cargo = header['Cargo $']
                    cargo_format = cargo.replace('.','') if '.' in cargo else cargo
                    abono_format = abono.replace('.','') if '.' in abono else abono
                    values['amount'] = float(cargo_format) * -1 if float(cargo_format) != 0 else abono_format
                    values['statement_id'] = active_id
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'estado':
                contador = 17
                header = {}
                values_header = [sheet.cell_value(16, i) for i in range(sheet.ncols)]
                for row_no in range(17, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if header['Fecha'] == 'Resumen:':
                        break
                    if header['Fecha']:
                        date_format = header['Fecha'][0:10]
                        values['date'] = datetime.strptime(date_format, '%d-%m-%Y').strftime('%Y-%m-%d')
                    if header['Cheques/'] == 'Cargos $':
                        header['Cheques/'] = ''
                    if header['Depósitos/'] == 'Abonos $':
                        header['Depósitos/'] = ''
                    if header['Depósitos/'] and header['Depósitos/'] != '':
                        values['amount'] = header['Depósitos/']
                    if header['Cheques/'] and header['Cheques/'] != '':
                        values['amount'] = header['Cheques/']
                    if header['Descripción']:
                        values['payment_ref'] = header['Descripción']
                        bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'scotiabank':
                contador = 11
                header = {}
                values_header = [sheet.cell_value(10, i) for i in range(sheet.ncols)]
                for row_no in range(11, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if not header['Fecha']:
                        break
                    values['statement_id'] = active_id
                    if header['Cargo']:
                        values['amount'] = header['Cargo'] * -1
                    else:
                        values['amount'] = header['Abono'] 
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d-%m-%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    bank_statement.write({'line_ids': [(0, 0, values)]})
            else:
                # ITAU Este es el fin y se recorre invertido
                contador = 26
                header = {}
                years_format = str(years)
                values_header = [sheet.cell_value(25, i) for i in range(sheet.ncols)]
                for row_no in range(26, sheet.nrows):
                    contador += 1
                    for col in range(sheet.ncols):
                        header[values_header[col]] = sheet.cell_value(row_no, col)
                    if header['Fecha'] == 'Resumen de Saldos':
                        break
                    values['statement_id'] = active_id
                    if header['Fecha']:
                        fecha_fomat = header['Fecha'] + '/' + years_format
                        values['date'] = datetime.strptime(fecha_fomat, '%d/%m/%Y').strftime('%Y-%m-%d')
                    abonos = header['Depósitos'] = '' if header['Depósitos'] == 'o abonos' else header['Depósitos']
                    cargos = header['Giros'] = '' if header['Giros'] == 'o cargos' else header['Giros']
                    if cargos != '' or abonos != '':
                        values['amount'] = abonos if abonos else cargos
                    if header['Descripción'] != '':
                        values['payment_ref'] = header['Descripción']
                        bank_statement.write({'line_ids': [(0, 0, values)]})
        else:
            raise Warning('Please Select File Type')
        self.env['account.bank.statement'].browse(self._context.get('active_id'))._end_balance()
        return res

    #@api.model
    def _create_statement_lines(self, val):
        partner_id = self._find_partner(val.get('partner'))
        if not val.get('date'):
            raise Warning('Please Provide Date Field Value')
        if not val.get('memo'):
            raise Warning('Please Provide Memo Field Value')
        aaa = self._cr.execute(
            "insert into account_bank_statement_line (date,ref,partner_id,name,amount,statement_id) values (%s,%s,%s,%s,%s,%s)",
            (val.get('date'), val.get('ref'), partner_id, val.get('memo'), val.get('amount'),
             self._context.get('active_id')))
        return True

    def _find_partner(self, name):
        partner_id = self.env['res.partner'].search([('name', '=', name)])
        if partner_id:
            return partner_id.id
        else:
            return
