"""PytSite Wallet Endpoints
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, router as _router
from plugins import odm as _odm, admin as _admin
from . import _forms, _model


class TransactionsCancel(_routing.Controller):
    def exec(self):
        browse_url = _router.rule_url('odm_ui@admin_browse', {'model': 'wallet_transaction'})

        ids = self.arg('ids')
        if not ids:
            return self.redirect(browse_url)

        if isinstance(ids, str):
            ids = (ids,)

        frm = _forms.TransactionsCancel(uid='odm-ui-d-form', model='wallet_transaction', eids=ids)

        return _admin.render(str(frm))


class TransactionsCancelSubmit(_routing.Controller):
    def exec(self):
        ids = self.arg('ids')
        if not ids:
            return self.redirect(_router.request().inp.get('__redirect'))

        if isinstance(ids, str):
            ids = (ids,)

        for eid in ids:
            entity = _odm.dispense('wallet_transaction', eid)  # type: _model.Transaction
            if not entity.authorize_action('cancel'):
                raise self.unauthorized()

            entity.cancel()

        redirect = self.arg('__redirect', _router.rule_url('odm_ui@admin_browse', {'model': 'wallet_transaction'}))

        return self.redirect(redirect)
