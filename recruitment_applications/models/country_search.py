# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CountrySearch(models.Model):
    _name = "country_search"

    name = fields.Char(string="In which country you can search")
