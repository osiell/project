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

from odoo import fields, models, api


class project_timebox_fill(models.TransientModel):
    _name = 'project.timebox.fill.plan'
    _description = 'Project Timebox Fill'

    @api.model
    def _get_from_tb(self):
        timeboxes = self.env['project.gtd.timebox'].search([])
        return timeboxes and timeboxes[0] or False

    @api.model
    def _get_to_tb(self):
        return self.env.context.get('active_id')

    timebox_id = fields.Many2one(
        'project.gtd.timebox', 'Get from Timebox', required=True,
        default=_get_from_tb)
    timebox_to_id = fields.Many2one(
        'project.gtd.timebox', 'Set to Timebox', required=True,
        default=_get_to_tb)
    task_ids = fields.Many2many(
        'project.task',
        'project_task_rel', 'task_id', 'fill_id',
        'Tasks selection')

    @api.model
    def process(self):
        if not self.env.ids:
            return {}
        data = self.read([])
        if not data[0]['task_ids']:
            return {}
        self.env['project.task'].browse(data[0]['task_ids']).write(
            {'timebox_id': data[0]['timebox_to_id'][0]})
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
