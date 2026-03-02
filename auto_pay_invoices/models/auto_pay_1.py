from odoo import models, fields, api


class AutoPay1(models.Model):

    _inherit = 'account.move'

    @api.model
    def cron_auto_pay_all_invoices_1(self):

        # Only posted invoices that are not showing as paid
        invoices = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid')
        ])

        for invoice in invoices:
            # If invoice is fully paid (residual is 0), force payment_state update
            if invoice.amount_residual <= 0:
                # Trigger compute by writing the same value
                invoice.write({'invoice_date': invoice.invoice_date or False})

