from odoo import models, fields


class Sessions(models.Model):
    _name = 'open.session'
    _description = 'session is an occurrence of a course taught at a given time for a given audience.'
    
    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Integer(string="Duration (Hours)")
    number_of_seat = fields.Integer()
    course_id = fields.Many2one('open.course', 
                                ondelete='cascade', 
                                string='Course', 
                                required=True)
    instructor_id = fields.Many2one('res.partner', 
                                    ondelete='set null', 
                                    string='Instructor')
    attendees_ids = fields.Many2many('res.partner',
                                     string='Attendees')