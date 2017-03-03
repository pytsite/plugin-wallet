"""PytSite Wallet Package.
"""
# Public API
from . import _error as error, _model as model
from . import _field as field, _widget as widget
from ._api import create_account, get_account, create_transaction, commit_transactions_1, commit_transactions_2, \
    cancel_transactions_1, cancel_transactions_2


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import lang, odm, admin, router, events, assetman, permissions
    from . import _eh

    # Resources
    lang.register_package(__name__, alias='wallet')
    assetman.register_package(__name__, alias='wallet')

    # Permission group
    permissions.define_group('wallet', 'wallet@wallet')

    # ODM models
    odm.register_model('wallet_account', model.Account)
    odm.register_model('wallet_transaction', model.Transaction)

    # Admin sidebar entries
    admin.sidebar.add_section('wallet', 'wallet@wallet', 250)
    admin.sidebar.add_menu('wallet', 'accounts', 'wallet@accounts',
                           router.ep_path('pytsite.odm_ui@browse', {'model': 'wallet_account'}),
                           'fa fa-credit-card', weight=10, permissions='pytsite.odm_auth.view.wallet_account')
    admin.sidebar.add_menu('wallet', 'transactions', 'wallet@transactions',
                           router.ep_path('pytsite.odm_ui@browse', {'model': 'wallet_transaction'}),
                           'fa fa-exchange', weight=20, permissions='pytsite.odm_auth.view.wallet_transaction')

    # Cron event dispatcher
    events.listen('pytsite.cron.1min', _eh.cron_1_min)

    # Admin routes
    abp = admin.base_path()
    router.handle(abp + '/odm_ui/wallet_transaction/cancel', 'plugins.wallet@transactions_cancel')
    router.handle(abp + '/odm_ui/wallet_transaction/cancel/submit', 'plugins.wallet@transactions_cancel_submit')


__init()
