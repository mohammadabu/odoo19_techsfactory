from odoo import models, fields, api,exceptions

class Custom_Invoice(models.Model):
    _inherit = 'account.move'
    

    invoice_date = fields.Date(string='Invoice/Bill Date111',copy=False)

    def write(self, vals):
        if 'invoice_date' in vals:
            # Bypass posted restriction
            return super(
                Custom_Invoice,
                self.with_context(
                    skip_account_move_synchronization=True,
                    check_move_validity=False,
                    skip_invoice_sync=True,
                )
            ).write(vals)

        return super().write(vals)



    def _check_write_allowed(self, fields):
        # Allow editing invoice_date on posted moves (LOCAL ONLY)
        if 'invoice_date' in fields:
            return
        return super()._check_write_allowed(fields)
