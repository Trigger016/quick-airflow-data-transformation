from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean()
    session_ids = fields.Many2many('open.session',
                                   string='Sessions')