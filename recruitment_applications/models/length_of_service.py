# -*- coding: utf-8 -*-
from odoo import api, fields, models


class LengthOfService(models.Model):
    _name = "length_of_service"

    name = fields.Char(string="Length of service")
