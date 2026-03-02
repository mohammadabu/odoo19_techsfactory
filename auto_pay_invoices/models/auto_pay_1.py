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

        if not invoices:
            return

        bank_journal = self.env['account.journal'].search([
            ('type', '=', 'bank')
        ], limit=1)

        if not bank_journal:
            return

        for invoice in invoices:

            if invoice.amount_residual <= 0:
                continue

            payment_vals = {
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': invoice.partner_id.id,
                'amount': invoice.amount_residual,
                'journal_id': bank_journal.id,
                'payment_method_line_id': bank_journal.inbound_payment_method_line_ids[:1].id,
                'date': invoice.invoice_date or fields.Date.today(),
                'ref': f'Auto Payment for {invoice.name}',
            }

            payment = self.env['account.payment'].create(payment_vals)

            payment.action_post()

            # Reconcile receivable lines
            lines = (invoice.line_ids + payment.move_id.line_ids).filtered(
                lambda l: l.account_id == invoice.partner_id.property_account_receivable_id
                and not l.reconciled
            )

            if lines:
                lines.reconcile()