from odoo import models, fields, api, exceptions,_


class StudentGroup(models.Model):
    _name = 'pfe.sgroupe'
    _description = 'Student Group'
    _order = 'group_avg desc'
    _rec_name = 'G_name'
    name = fields.Char(
        string="Group Ref",
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )

    G_name = fields.Char(string='Group Name', required=False)
    compute = fields.Integer(compute='com', string='sequence')
    specialization_id = fields.Many2one('pfe.specialization', string='Specialization', required=False)
    education_level_id = fields.Many2one('pfe.education_level', string='Education Level', required=False)
    choose_id = fields.One2many('pfe.choose_list', 'group_id', string="Choose List", required=True)
    leader_id = fields.Many2one(
        'hr.employee', string='Group Leader',
        domain=[('is_student', '=', True)], required=True
    )

    student_ids = fields.One2many(
        'hr.employee',
        'group_id',
        string='Group Members',
        domain=[('is_student', '=', True)]
    )

    group_avg = fields.Float(string='Group Average', compute='_compute_group_avg', store=True)
    leader_user_id = fields.Many2one('res.users', string="Leader User", compute="_compute_leader_user", store=True)

    academic_year_id = fields.Many2one(
        'event.event',
        string="Academic Year",
    )

    selected_dissertation_id = fields.Many2one(
        comodel_name='pfe.dissertation',
        string='Selected Dissertation'
    )

    @api.depends('student_ids.avg_grade')
    def _compute_group_avg(self):
        for group in self:
            students_with_grades = [student.avg_grade for student in group.student_ids if student.avg_grade > 0]
            group.group_avg = sum(students_with_grades) / len(students_with_grades) if students_with_grades else 0.0

    @api.constrains('student_ids', 'leader_id')
    def _check_group_constraints(self):
        for group in self:
            if group.leader_id and group.leader_id not in group.student_ids:
                group.update({'student_ids': [(4, group.leader_id.id)]})

            if len(group.student_ids) > 3:
                raise exceptions.ValidationError("المجموعة يجب أن تتكون من القائد و 2 طلاب كحد أقصى.")

            specializations = {s.specialization_id.id for s in group.student_ids}
            levels = {s.education_level_id.id for s in group.student_ids}

            if len(specializations) > 1:
                raise exceptions.ValidationError("يجب أن يكون جميع الأعضاء من نفس التخصص.")
            if len(levels) > 1:
                raise exceptions.ValidationError("يجب أن يكون جميع الأعضاء من نفس المستوى التعليمي.")

    @api.depends('leader_id')
    def _compute_leader_user(self):
        for group in self:
            group.leader_user_id = group.leader_id.user_id if group.leader_id else False

    @api.model
    def is_student(self):
        return self.env.user.has_group('pfe.group_student')

    @api.model
    def get_my_group(self):
        if not self.is_student():
            return {'error': "أنت لست طالبًا"}

        student = self.env.user.employee_id
        my_group = self.search([('student_ids', 'in', student.id)], limit=1)

        return {
            'group_name': my_group.name if my_group else "لا تنتمي إلى أي مجموعة",
            'students': my_group.student_ids.mapped('name') if my_group else []
        }

    @api.model
    def assign_topics_by_choice_and_average(self):
        groupes = self.search([], order='group_avg desc')  # جلب كل المجموعات مرتبة حسب المعدل

        for groupe in groupes:
            if groupe.selected_dissertation_id:
                continue  # إذا لديه موضوع معين بالفعل نتخطى

            # ترتيب الاختيارات حسب sequence
            choix_tries = sorted(groupe.choose_id, key=lambda c: c.sequence)
            for choix in choix_tries:
                dissertation = choix.dissertation_id
                # نتأكد من أن موضوع الأطروحة (topic) في حالة 'validated'
                # وأن الأطروحة لم تُخصص لمجموعة أخرى بعد
                if dissertation and dissertation.topic_id.state == 'validated' and not dissertation.group_id:
                    groupe.selected_dissertation_id = dissertation.id
                    dissertation.group_id = groupe.id
                    break

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pfe.sgroupe') or _('New')
        return super(StudentGroup, self).create(vals)
