# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, exceptions
from odoo.tools.translate import _


class project_timebox_empty(models.TransientModel):
    _name = 'project.timebox.empty'
    _description = 'Project Timebox Empty'

    name = fields.Char('Name', size=32)

    @api.model
    def view_init(self, fields_list):
        self._empty()

    def _empty(self):
        close = []
        up = []
        timebox_model = self.env['project.gtd.timebox']
        task_model = self.env['project.task']

        if 'active_id' not in self.env.context:
            return {}

        timeboxes = timebox_model.search([])
        if not timeboxes:
            raise exceptions.UserError(
                _('No timebox child of this one!'))
        tasks = task_model.search([
            ('timebox_id', '=', self.env.context['active_id'])])
        for task in tasks:
            if (task.stage_id and task.stage_id.fold) \
                    or (task.user_id.id != self.env.uid):
                close.append(task.id)
            else:
                up.append(task.id)
        if up:
            task_model.browse(up).write({'timebox_id': timeboxes[0].id})
        if close:
            task_model.browse(close).write({'timebox_id': False})
        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
