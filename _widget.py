"""PytSite Wallet Widgets
"""
from decimal import Decimal as _Decimal
from frozendict import frozendict as _frozendict
from pytsite import html as _html
from plugins import widget as _w, auth as _auth, odm as _odm, currency as _currency

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AccountSelect(_w.select.Select):
    """Wallet Account Select Widget
    """

    def __init__(self, uid: str, **kwargs):
        u = _auth.get_current_user()
        items = []

        f = _odm.find('wallet_account').sort([('title', _odm.I_ASC)])

        # Ordinary user can only view its own accounts
        if not u.is_admin:
            f.eq('owner', u.uid)

        for acc in f.get():
            label = '{} ({})'.format(acc.title, acc.currency)
            items.append(('wallet_account:' + str(acc.id), label))

        super().__init__(uid, items=items, **kwargs)


class MoneyInput(_w.Abstract):
    """Money Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._default_currency = kwargs.get('default_currency', _currency.get_main())
        if self._default_currency not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(self._default_currency))

        self._currency_select = kwargs.get('currency_select', False)
        self._css += ' widget-wallet-money-input'
        self._js_modules.append('wallet-widget-input-money')

    def set_val(self, value: dict):
        """Set value of the widget.
        """
        # 'Empty' value
        if value is None:
            value = {'amount': _Decimal('0.0'), 'currency': self._default_currency}

        # Checking input
        if type(value) not in (dict, _frozendict):
            raise ValueError('Dict expected.')

        # Convert input to mutable dict
        if isinstance(value, _frozendict):
            value = dict(value)

        # Checking input parts
        if 'currency' not in value or not value['currency']:
            raise ValueError("Value of the widget '{}' must contain 'currency' key.".format(self._name))
        if 'amount' not in value:
            raise ValueError("Value of the widget '{}' must contain 'amount' key.".format(self._name))

        # Checking currency validness
        if value['currency'] not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value['currency']))

        # Processing string input
        if isinstance(value['amount'], str) and not value['amount'].strip():
            value['amount'] = _Decimal(0)

        # Processing float input
        if isinstance(value['amount'], float):
            value['amount'] = str(value['amount'])

        # Processing another inputs
        if not isinstance(value['amount'], _Decimal):
            value['amount'] = _Decimal(value['amount'])

        self._value = _frozendict(value)

        return self

    def _get_element(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.
        """
        # Container
        r = _html.Div()

        # Text input for amount
        r.append(_html.Input(
            type='tel',
            name=self.uid + '[amount]',
            value=round(self._value['amount'], 2),
            css='amount form-control',
        ))

        if self._currency_select:
            # Currency select
            r.set_attr('css', 'inputs-wrapper')
            sel = _html.Select(
                uid=self.uid + '[currency]',
                name=self.uid + '[currency]',
                css='currency-select form-control'
            )

            for code in _currency.get_all():
                if not code.startswith('_'):
                    selected = True if code == self._value['currency'] else False
                    sel.append(_html.Option(code, value=code, selected=selected))

            r.append(sel)
        else:
            # Currency static add-on
            r.set_attr('css', 'input-group')
            r.append(_html.Span(_currency.get_symbol(self._value['currency']), css='input-group-addon'))
            r.append(_html.Input(type='hidden', name=self._uid + '[currency]', value=self._value['currency']))

        return r
