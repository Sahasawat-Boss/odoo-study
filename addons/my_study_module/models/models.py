from odoo import fields, models


class StudyNote(models.Model):
    _name = 'study.note'
    _description = 'Study Note'
    _order = 'date desc, id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.context_today)
