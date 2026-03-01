from odoo import models, fields, api,exceptions

class Custom_Invoice(models.Model):
    _inherit = 'account.move'
    

    invoice_date = fields.Date(string='Invoice/Bill Date111',copy=False)

    def write(self, vals):
        if 'invoice_date' in vals:
            self = self.with_context(check_move_validity=False)
        return super().write(vals)
