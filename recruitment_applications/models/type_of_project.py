# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TypeOfProject(models.Model):
    _name = "type_of_project"

    name = fields.Char(string="Name of project type")
