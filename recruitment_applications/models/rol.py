# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Rol(models.Model):
    _name = "rol"

    name = fields.Char(string="Role name")
