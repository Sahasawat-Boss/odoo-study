from odoo import api, fields, models


class StudyNote(models.Model):
    _name = 'study.note'
    _description = 'Study Note'
    _order = 'done, priority desc, date desc, id desc'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    # NEW 1: ความสำคัญ แสดงเป็นดาว ⭐ ด้วย widget="priority" ใน view
    priority = fields.Selection(
        [('0', 'Normal'), ('1', 'Important'), ('2', 'Very Important'), ('3', 'Urgent')],
        string='Priority', default='0',
    )

    # NEW 2: สถานะเสร็จแล้วหรือยัง
    done = fields.Boolean(string='Done', default=False)

    # NEW 3: compute field คำนวณอัตโนมัติจาก description ไม่ต้องกรอกเอง
    word_count = fields.Integer(string='Words', compute='_compute_word_count', store=True)

    @api.depends('description')
    def _compute_word_count(self):
        for note in self:
            note.word_count = len((note.description or '').split())

    # NEW 4: method ที่ปุ่ม "Mark as Done" ในหน้า form เรียกใช้
    def action_mark_done(self):
        self.done = True

    def action_reopen(self):
        self.done = False
