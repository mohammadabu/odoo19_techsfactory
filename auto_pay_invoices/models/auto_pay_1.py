from odoo import models, fields, api


class AutoPay1(models.Model):

    _inherit = 'account.move'

    @api.model
    def cron_auto_pay_all_invoices_1(self):

        invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid')
        ])

        # Force payment_state = 'paid' by writing directly
        invoices.write({'payment_state': 'paid'})