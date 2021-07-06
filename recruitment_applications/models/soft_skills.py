# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SoftSkills(models.Model):
    _name = "soft_skills"

    name = fields.Char(string="Soft skills")
