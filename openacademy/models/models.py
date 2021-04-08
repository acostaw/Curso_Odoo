# -*- coding: utf-8 -*-
# llos tipos de datos siempre tiene que empezar con la Mayuscula
from datetime import timedelta
from odoo import api, fields, models, exceptions


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Open Academy Courses'

    name = fields.Char(string="Titulo", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users', ondelete='set null', string='Responsable')
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sesiones")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count([('name', '=like',u"Copia de {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copia de {}".format(self.name)
        else:
            new_name = u"Copia de {} ({})".format(self.name,copied_count)
        default['name'] = new_name
        return super(Course,self).copy(default)




    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "El titulo del curso no debe ser igual a la descripcion "),

        ('name_unique',
        'UNIQUE(name)',
        "El nombre del  curso debe ser único"),
        
    ]



class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string="Nombre", required=True)
    start_date = fields.Date(string="Fecha de Inicio", default=fields.Date.today)
    duration = fields.Float(digits = (6,2), help="Duracion en Días")
    seats = fields.Integer(string="Numero de Asiento")
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor", 
    domain=['|',('instructor','=',True),('category_id.name','ilike','Profesor')])
    course_id = fields.Many2one('openacademy.course', string="Curso", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Asistentes")

    taken_seats = fields.Float(string="Asientos Ocupados", compute='_taken_seats')
    end_date = fields.Date(string="Fecha Fin", store = True, compute='_get_end_date', 
    inverse='_set_end_date')
    color = fields.Integer()


    attendee_count = fields.Integer(string="Cantidad Asientos", compute="_get_attendees_count", store=True )
    

    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for r in self:

            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
                self.field_name = ''

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendee_count = len(r.attendee_ids)
    

    @api.depends('start_date','duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date=r.start_date
                continue
            start = fields.Date.from_string(r.start_date)
            duration = timedelta(days=r.duration,seconds=-1)
            r.end_date = start + duration
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1


           
    #onchage
    @api.onchange('seats','attendee_ids')
    def _verify_valid_seats(self):
        if self.seats  < 0:
            return {
                'warning':{
                    'title':"Numero incorrecto de asientos",
                    'message':"La cantidad de asientos disponibles puede no ser negativo",
                },
            }
        if self.seats  < len(self.attendee_ids):
            return {
                'warning':{
                    'title':"Demasiado Alumnos",
                    'message':"Aumentar el numero de asientos o limitar el numero de alumnos",

                },
            }
    @api.constrains('instructor_id','attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("El instructor de una sesion no puede ser asistente")

        
    