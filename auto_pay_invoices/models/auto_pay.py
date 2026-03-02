from odoo import models, fields, api


class AccountMove213213321321(models.Model):

    _inherit = 'account.move'

    @api.model
    def cron_auto_pay_all_invoices_1(self):
        # Get all posted invoices
        invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ])

        for invoice in invoices:
            # Force recompute payment_state
            invoice._compute_payment_state()

        # Update payment state of payments as well
        payments = self.env['account.payment'].search([
            ('state', '=', 'posted')
        ])

        for payment in payments:
            # Force recompute is_posted or status check
            payment._compute_payment_state()

