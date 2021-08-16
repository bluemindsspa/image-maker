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
        ('itau', 'Banco Itau'), ('tdci', 'TC Internacional Banco Chile'), ('tdcn', 'TC Nacional Banco Chile')])

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
                    if header['MONTO'] == 'Resumen comisiones':
                        break
                    if header['MONTO'] == 'Saldos diarios':
                         break

                    values['statement_id'] = active_id
                    values['amount'] = header['MONTO']
                    values['date'] = datetime.strptime(
                        header['FECHA'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['DESCRIPCIÓN MOVIMIENTO']
                    # vals['amount'] = values_es['MONTO']
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
                    if header['Fecha'] == 'Saldo (CLP)':
                        break
                    

                    values['statement_id'] = active_id
                    values['amount'] = header['Cargos (CLP)']
                    values['amount'] = header['Abonos (CLP)']
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    # vals['amount'] = values_es['MONTO']
                    #values['narration'] = header['CARGO/ABONO']

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
                    values['amount'] = header['Montos']
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
                    values['amount'] = header['Monto Moneda Origen']
                    #values['amount'] = header['Abonos (CLP)']
                    values['date'] = datetime.strptime(
                        header['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    values['payment_ref'] = header['Descripción']
                    # vals['amount'] = values_es['MONTO']
                    #values['narration'] = header['CARGO/ABONO']

                    bank_statement.write({'line_ids': [(0, 0, values)]})
            elif self.bank_opt == 'estado':
                for row_no in range(sheet.nrows):

                    if row_no <= 0:
                        fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                    else:
                        line = list(
                            map(lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value),
                                sheet.row(row_no)))

                        date_string = line[5]
                        date_string = date_string[:10]
                        try:
                            date_string = datetime.strptime(date_string, '%d/%m/%Y').strftime('%Y-%m-%d')
                        except:
                            date_string = '01-01-01'
                            contador = contador + 1
                        if date_string != '01-01-01' and contador <= 100:
                            contador = 100
                            # if line[3] in (None, "", 0, '0'):
                            if line[3] <= line[4] or (line[3] in (None, "", 0, '0', "0")):
                                values.update({'date': date_string,
                                               'ref': line[0].decode("utf-8"),
                                               'partner': line[6],
                                               'memo': line[1].decode("utf-8"),
                                               'amount': int(line[4].replace('.', '')) / 10,
                                               })
                            else:
                                values.update({'date': date_string,
                                               'ref': line[0].decode("utf-8"),
                                               'partner': line[6],
                                               'memo': line[1].decode("utf-8"),
                                               # 'amount': line[3] * (-1),
                                               'amount': int(line[3].replace('.', '')) * (-1) / 10,
                                               })
                            res = self._create_statement_lines(values)
            else:
                # ITAU Este es el fin y se recorre invertido
                for row_no in range(sheet.nrows):

                    if row_no <= 26:
                        fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                    else:
                        line = list(
                            map(lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value),
                                sheet.row(row_no)))
                        # data = line[].decode("utf-8"

                        if line[0] != '':
                            fecha = line[0].decode("utf-8")
                            fecha = fecha + '/' + str(years)

                            try:
                                date_string = datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
                                if line[3] != 0 and line[3] != '':
                                    monto = int(line[3].replace('.0', ''))

                                    values.update({'date': date_string,
                                                   'ref': line[2].decode("utf-8"),
                                                   'partner': 'X',
                                                   'memo': line[2].decode("utf-8"),
                                                   'amount': monto * (-1),
                                                   })
                                if line[3] == 0 and line[3] != '':
                                    values.update({'date': date_string,
                                                   'ref': line[2].decode("utf-8"),
                                                   'partner': 'X',
                                                   'memo': line[2].decode("utf-8"),
                                                   'amount': int(line[4].replace('.0', '')),
                                                   })
                                res = self._create_statement_lines(values)
                            except:
                                break






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
