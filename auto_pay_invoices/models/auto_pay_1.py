from odoo import models, fields, api


class AutoPay1(models.Model):

    _inherit = 'account.move'

    @api.model
    def cron_auto_pay_all_invoices_1(self):

        # Only posted invoices that are not showing as paid
        invoices = self.search([
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid')
        ])

        for invoice in invoices:
            # Get all posted payments linked to this invoice
            payments = self.env['account.payment'].search([
                ('state', '=', 'posted'),
                ('partner_id', '=', invoice.partner_id.id)
            ])

            # Filter payments that are fully reconciled with this invoice
            for payment in payments:
                lines_to_reconcile = (invoice.line_ids + payment.move_id.line_ids).filtered(
                    lambda l: l.account_id == invoice.partner_id.property_account_receivable_id and not l.reconciled
                )
                if lines_to_reconcile:
                    lines_to_reconcile.reconcile()


