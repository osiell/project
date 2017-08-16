# -*- coding: utf-8 -*-
# Copyright 2017 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, tools


class project_gtd_context(models.Model):
    _name = "project.gtd.context"
    _description = "Context"
    _order = "sequence, name"

    name = fields.Char(
        'Context', size=64, required=True, translate=True)
    sequence = fields.Integer(
        'Sequence',
        help=("Gives the sequence order when displaying a list of contexts."),
        default=1)


class project_gtd_timebox(models.Model):
    _name = "project.gtd.timebox"
    _order = "sequence"

    name = fields.Char(
        'Timebox', size=64, required=True, index=1, translate=1)
    sequence = fields.Integer(
        'Sequence',
        help="Gives the sequence order when displaying "
             "a list of timebox.")


class project_task(models.Model):
    _inherit = "project.task"

    @api.model
    def _get_context(self):
        contexts = self.env['project.gtd.context'].search([])
        return contexts and contexts[0] or False

    timebox_id = fields.Many2one(
        'project.gtd.timebox',
        "Timebox",
        help="Time-laps during which task has to be treated")
    context_id = fields.Many2one(
        'project.gtd.context',
        "Context",
        help="The context place where user has to treat task",
        default=_get_context)

    def _read_group_timebox_ids(
            self, domain, read_group_order=None, access_rights_uid=None):
        """Used to display all timeboxes on the view."""
        timebox_model = self.env['project.gtd.timebox']
        timeboxes = timebox_model.search([])
        timebox_ids = timeboxes.ids
        result = timeboxes.name_get()
        # Restore order of the search
        result.sort(
            lambda x, y: cmp(timebox_ids.index(x[0]), timebox_ids.index(y[0])))
        fold = dict.fromkeys(timeboxes, False)
        return result, fold

    _group_by_full = {
        'timebox_id': _read_group_timebox_ids,
    }

    @api.model
    def copy_data(self, default=None):
        if not default:
            default = {}
        if not default.get('timebox_id'):
            default['timebox_id'] = False
        if not default.get('context_id'):
            default['context_id'] = False
        return super(project_task, self).copy_data(default)

    #  def next_timebox(self, cr, uid, ids, *args):
    #      timebox_obj = self.pool.get('project.gtd.timebox')
    #      timebox_ids = timebox_obj.search(cr, uid, [])
    #      if not timebox_ids:
    #          return True
    #      for task in self.browse(cr, uid, ids):
    #          timebox = task.timebox_id
    #          if not timebox:
    #              self.write(cr, uid, task.id, {'timebox_id': timebox_ids[0]})
    #          elif timebox_ids.index(timebox) != len(timebox_ids)-1:
    #              index = timebox_ids.index(timebox)
    #              self.write(
    #                  cr, uid, task.id, {'timebox_id': timebox_ids[index+1]})
    #      return True
    #
    #  def prev_timebox(self, cr, uid, ids, *args):
    #      timebox_obj = self.pool.get('project.gtd.timebox')
    #      timebox_ids = timebox_obj.search(cr, uid, [])
    #      for task in self.browse(cr, uid, ids):
    #          timebox = task.timebox_id
    #          if timebox:
    #              if timebox_ids.index(timebox):
    #                  index = timebox_ids.index(timebox)
    #                  self.write(
    #                      cr, uid, task.id,
    #                      {'timebox_id': timebox_ids[index - 1]})
    #              else:
    #                  self.write(cr, uid, task.id, {'timebox_id': False})
    #      return True

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(project_task, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        timebox_model = self.env['project.gtd.timebox']
        if (res['type'] == 'search') and self.env.context.get('gtd', False):
            timeboxes = timebox_model.search([])
            search_extended = ''
            for timebox in timeboxes:
                filter_ = u"""
                    <filter domain="[('timebox_id', '=', {timebox_id})]"
                            string="{string}"/>\n
                    """.format(timebox_id=timebox.id, string=timebox.name)
                search_extended += filter_
            search_extended += '<separator orientation="vertical"/>'
            res['arch'] = tools.ustr(res['arch']).replace(
                '<separator name="gtdsep"/>', search_extended)

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
