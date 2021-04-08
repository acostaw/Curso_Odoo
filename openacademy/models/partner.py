# comando para crear omodi
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many("openacademy.session", string="Sesiones Asistidas", readonly=True)