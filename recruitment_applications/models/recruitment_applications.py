# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Job(models.Model):
    _name = 'hr.job'
    _inherit = ['hr.job', 'mail.thread']

    rol_id = fields.Many2one('rol', string="Rol")
    application_status_id = fields.Many2one(
        'application_status',
        string="Application status",
        tracking=True)
    proposal_reference_id = fields.Many2one(
        'sale.order',
        string="Proposal reference")
    assigned = fields.Many2many('res.users', string="Assigned:")
    revisor_id = fields.Many2one('res.users', string="Revisor")
    partner_id = fields.Many2one('res.partner', string="Client")
    solicitante_id = fields.Many2one(
        'res.users', copy=False, tracking=True,
        string="Solicitante", default=lambda self: self.env.user)
    customer_leader_id = fields.Many2one(
        'res.partner',
        string="Customer leader")
    priority = fields.Selection([
        ('0', 'short'),
        ('1', 'normal'),
        ('2', 'hard'),
        ('3', 'complicated')],
        string="Priority")
    account_item_id = fields.Many2one(
        'account_item',
        string="Account item")
    location_id = fields.Many2one(
        'location',
        string="Customer location")
    vacancies = fields.Integer(string="Vacancies")
    work_address = fields.Many2one(
        'res.partner',
        string="Work address")
    working_hours = fields.Float(string="Working hours")
    since = fields.Float(string="Since")
    until = fields.Float(string="Until")
    additional_benefits = fields.Text(string="Additional benefits")
    type_of_opportunities_id = fields.Many2one(
        'type_of_oportunities',
        string="Type of opportunities")
    maker_to_replace_id = fields.Many2one(
        'res.users',
        string="Maker to replace ")
    area_im_id = fields.Many2one(
        'hr.department',
        string="Area IM")
    includes_referral = fields.Boolean(string="Includes referral?")
    monday = fields.Boolean(string="Lu")
    tuesday = fields.Boolean(string="Ma")
    wednesday = fields.Boolean(string="Mi")
    thursday = fields.Boolean(string="Ju")
    friday = fields.Boolean(string="Vi")
    saturday = fields.Boolean(string="Sa")
    sunday = fields.Boolean(string="Do")
    length_of_service_id = fields.Many2one(
        'length_of_service',
        string="Length of service")
    estimated_date_of_entry = fields.Date(string="Estimated date of entry")
    income_ceiling_id = fields.Many2one(
        'income_ceiling',
        string="Income ceiling")
    years_of_experience = fields.Integer(string="Years of experience")
    languages_id = fields.Many2many(
        'languages',
        string="Languages")
    type_of_project_id = fields.Many2one(
        'type_of_project',
        string="Type of project")
    job_functions = fields.Char(string="Job functions")
    exclusive_technical_requirements = fields.Text(
        string="Technical requirements")
    desirable_academic_requirements = fields.Char(
        string="Desirable academic requirements")
    desirable_technical_requirements = fields.Text(string="Desirable technical requirements")
    soft_skills = fields.Text(
        string="Soft skills")
    can_you_reside_abroad = fields.Boolean(string="Can you reside abroad ?")
    country_search_id = fields.Many2many(
        'country_search',
        string="In which country you can search")
    customer_request_document = fields.Boolean(
        string="Customer request document")
    archivo = fields.Binary(string="Documento del cliente")
    referido = fields.Binary(string="Referido")
