# -*- coding: utf-8 -*-
from odoo import api, fields, models


class IncomeCeiling(models.Model):
    _name = "income_ceiling"

    name = fields.Char(string="Income ceiling")
