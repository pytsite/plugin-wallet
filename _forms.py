"""PytSite Wallet Forms
"""
from pytsite import router as _router, metatag as _metatag, lang as _lang, http as _http
from plugins import odm_ui as _odm_ui, odm_auth as _odm_auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TransactionsCancel(_odm_ui.forms.MassAction):
    """Transactions Cancel Form.
    """
    def _on_setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        super()._on_setup_form()

        # Check permissions
        for eid in self._eids:
            if not _odm_auth.check_permission('cancel', self._model, eid):
                raise _http.error.Unauthorized()

        # Action URL
        self._action = _router.rule_url('plugins.wallet@transactions_cancel_submit')

        # Page title
        _metatag.t_set('title', _lang.t('wallet@odm_ui_form_title_cancel_' + self._model))

    def _on_setup_widgets(self):
        """Hook.
        """
        super()._on_setup_widgets()

        # Change submit button color
        self.get_widget('action-submit').color = 'danger'
