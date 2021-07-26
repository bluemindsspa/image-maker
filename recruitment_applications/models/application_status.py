# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ApplicationStatus(models.Model):
    _name = "application_status"

    name = fields.Char(string="Application status")
