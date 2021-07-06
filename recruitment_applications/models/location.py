# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Location(models.Model):
    _name = "location"

    name = fields.Char(string="Location")
