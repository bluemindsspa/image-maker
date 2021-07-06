# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TypeOfOportunities(models.Model):
    _name = "type_of_oportunities"

    name = fields.Char(string="Oportunities")
