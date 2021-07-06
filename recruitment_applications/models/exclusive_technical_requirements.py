# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ExclusiveTechnicalRequirements(models.Model):
    _name = "exclusive_technical_requirements"

    name = fields.Char(string="Exclusive technical requirements")
