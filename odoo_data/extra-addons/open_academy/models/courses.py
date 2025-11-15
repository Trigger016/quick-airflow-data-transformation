from odoo import models, fields, api


class Course(models.Model):
    _name = 'open.course'
    _description = 'Course table storing what its looks like title and description nonetheless.'

    title = fields.Char(required=True)
    description = fields.Char()
    resonsible_id = fields.Many2one('res.users', ondelete='set null',  
                                    string='Responsible')
    sessions_ids = fields.One2many('open.session', 
                                   'course_id',  
                                   string='Sessions')
    skill = fields.Selection([('FUNDAMENTAL', 'FUNDAMENTAL'), 
                              ('BEGINNER', 'BEGINNER'), ('INTERMEDIATE', 'INTERMEDIATE'), 
                              ('ADVANCE', 'ADVANCE')], 
                             string='Experience Level')