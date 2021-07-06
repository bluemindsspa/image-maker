# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Languages(models.Model):
    _name = "languages"

    name = fields.Char(string="Language")
