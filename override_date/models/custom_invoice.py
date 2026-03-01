from odoo import models, fields, api,exceptions
class Custom_Invoice(models.Model):
    _inherit = 'account.move'
    


    invoice_date = fields.Date(string='Invoice/Bill Date111')
