# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountItem(models.Model):
    _name = "account_item"

    name = fields.Char(string="Name of account item")
