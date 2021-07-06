# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DesirableTechnicalRequirements(models.Model):
    _name = "desirable_technical_requirements"

    name = fields.Char(string="Desirable technical requirements")
