from odoo import models, fields, api


class AutoPay1(models.Model):

    _inherit = 'account.move'

    @api.model
    def cron_auto_pay_all_invoices_1(self):

        # Find all posted invoices that are not showing as paid
        invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid')
        ])

        if not invoices:
            return

        # Force recompute of stored payment_state field
        invoices.invalidate_cache(['line_ids', 'amount_residual', 'payment_state'])
        invoices._compute_payment_state()  # recompute
        invoices._write({'payment_state': invoices.mapped('payment_state')})

        # Do the same for posted payments
        payments = self.env['account.payment'].search([
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid')
        ])

        if payments:
            payments.invalidate_cache(['move_line_ids', 'payment_state'])
            payments._compute_payment_state()
            payments._write({'payment_state': payments.mapped('payment_state')})

