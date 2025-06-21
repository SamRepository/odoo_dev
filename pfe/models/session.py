from odoo import models, fields, api

class EventEvent(models.Model):
    _inherit = 'event.event'

    department_id = fields.Many2one('hr.department', string='Département')

    @api.model
    def create(self, vals):
        event = super().create(vals)
        if vals.get('department_id'):
            event.action_email_to_department_student()
            event.action_email_to_department_teacher()
        return event

    def write(self, vals):
        res = super().write(vals)
        if 'department_id' in vals:
            self.action_email_to_department_student()
            self.action_email_to_department_teacher()
        return res

    def action_email_to_department_student(self):
        for event in self:
            if not event.department_id:
                continue

            students = self.env['hr.employee'].search([
                ('department_id', '=', event.department_id.id),
                ('is_student', '=', True),
                ('work_email', '!=', False),
            ])

            template = self.env.ref('pfe.email_template_event_student')
            for emp in students:
                template.send_mail(
                    event.id,
                    email_values={'email_to': emp.work_email},
                    force_send=True
                )

    def action_email_to_department_teacher(self):
        for event in self:
            if not event.department_id:
                continue

            teachers = self.env['hr.employee'].search([
                ('department_id', '=', event.department_id.id),
                ('category_ids.name', 'ilike', 'Teacher'),
                ('work_email', '!=', False),
                ('user_id', '!=', False),
            ])

            template = self.env.ref('pfe.email_template_event_teacher')

            for emp in teachers:
                template.send_mail(
                    event.id,
                    email_values={'email_to': emp.work_email},
                    force_send=True
                )
