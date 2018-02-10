"""PytSite Wallet Package.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error, _model as model
from . import _field as field, _widget as widget
from ._api import create_account, get_account, create_transaction, commit_transactions_1, commit_transactions_2, \
    cancel_transactions_1, cancel_transactions_2


def _register_resources():
    from pytsite import lang
    from plugins import assetman

    if not lang.is_package_registered(__name__):
        lang.register_package(__name__)

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.js_module('wallet-widget-input-money', __name__ + '@js/widget-input-money')
        assetman.t_less(__name__)
        assetman.t_js(__name__)


def plugin_install():
    from plugins import assetman

    _register_resources()
    assetman.build(__name__)


def plugin_load():
    from plugins import permissions, odm

    _register_resources()

    # Permission group
    permissions.define_group('wallet', 'wallet@wallet')

    # ODM models
    odm.register_model('wallet_account', model.Account)
    odm.register_model('wallet_transaction', model.Transaction)


def plugin_load_uwsgi():
    from pytsite import router, cron
    from plugins import admin
    from . import _eh, _controllers

    _register_resources()

    # Admin routes
    abp = admin.base_path()
    router.handle(_controllers.TransactionsCancel, abp + '/odm_ui/wallet_transaction/cancel',
                  'wallet@transactions_cancel')
    router.handle(_controllers.TransactionsCancelSubmit, abp + '/odm_ui/wallet_transaction/cancel/submit',
                  'wallet@transactions_cancel_submit')

    # Admin sidebar entries
    admin.sidebar.add_section('wallet', 'wallet@wallet', 250)
    admin.sidebar.add_menu('wallet', 'accounts', 'wallet@accounts',
                           router.rule_path('odm_ui@browse', {'model': 'wallet_account'}),
                           'fa fa-credit-card', weight=10, permissions='odm_auth@view.wallet_account')
    admin.sidebar.add_menu('wallet', 'transactions', 'wallet@transactions',
                           router.rule_path('odm_ui@browse', {'model': 'wallet_transaction'}),
                           'fa fa-exchange', weight=20, permissions='odm_auth@view.wallet_transaction')

    # Cron events
    cron.every_min(_eh.cron_1_min)
