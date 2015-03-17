# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2015 OpenERP SA (<http://www.serpentcs.com>)
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

from openerp.osv import fields, osv, expression
from openerp.tools.translate import _

class leads_category(osv.osv):
    
    _name = 'crm.leads.category'
    
    _columns = {
                'name' : fields.char('Name',required=True)
                }

class crm_lead(osv.osv):
    
    _inherit = "crm.lead"
    
    
    _columns ={
               'leads_category' : fields.many2one('crm.leads.category','Pool Category',required=True),
               'leads_reason' : fields.text('Leads Reason')
               }
    
    _defaults = {
                 'user_id' : False
                 }
    
    def cancel_leads(self,cr,uid,ids,context=None):
        if ids:
            cur_obj = self.browse(cr,uid,ids,context=context)
            for cur_id in cur_obj:
                if cur_id.leads_reason:
                    self.write(cr, uid, ids, {'stage_id': 1})
                else:
                    raise osv.except_osv(_('Message!'), _('Please write reason after cancel the leads.'))
        return True
    
    def assign_leads(self,cr,uid,ids,context=None):
        if ids:
            cur_obj = self.browse(cr,uid,ids,context=context)
            for cur_id in cur_obj:
                if cur_id.user_id:
                    stage_obj = self.pool.get('crm.case.stage')
                    stage_id = stage_obj.search(cr,uid,[('name','=','Assign')])
                    self.write(cr, uid, ids, {'stage_id': tuple(stage_id)})
                else:
                    raise osv.except_osv(_('Message!'), _('Please select sales person after assign Leads.'))
        return True
    
    
    def onselect_users(self,cr, uid, ids, leads_category, context=None):
        uesr_ids = []
        if leads_category:
            uesr_ids = self.pool.get('res.users').search(cr,uid,[('leads_category','=',leads_category)])
            return {
                    'domain': {
                               'user_id': [('leads_category', '=',leads_category)]
                               }
                    }
        else:
            return {
                    'domain': {
                               'user_id': [('leads_category', '=',[])]
                               }
                    }
        
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
