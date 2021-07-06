# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductionLot(models.Model):
	_inherit = 'stock.production.lot'

	employee_id = fields.Many2one('hr.employee', string='Empleado')
	imei_id = fields.Char(string='Imei')
	phone = fields.Char(string='N°- de Teléfono')
	description = fields.Text(string='Observaciones')
	license_ids = fields.Many2many('license.news')

class LicenseNews(models.Model):
	_name = "license.news"

	name = fields.Char('Nombre')