# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductionLot(models.Model):
	_inherit = 'stock.production.lot'

	employee_id = fields.Many2one('hr.employee', string='Empleado', tracking=True)
	imei = fields.Integer()
	phone = fields.Integer()
	description = fields.Text(string='Observaciones')
	license_ids = fields.Many2many('license.news')

class LicenseNews(models.Model):
	_name = "license.news"

	name = fields.Char('Nombre')