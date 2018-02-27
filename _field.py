"""PytSite Money ODM Field
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict as _frozendict
from decimal import Decimal as _Decimal
from plugins import auth as _auth, odm as _odm, currency as _currency


class Money(_odm.field.Dict):
    """PytSite Money ODM Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        # Default value
        if not kwargs.get('default'):
            u = _auth.get_current_user()
            currency = u.get_field('currency') if u and u.has_field('currency') else _currency.get_main()
            kwargs['default'] = {'currency': currency, 'amount': _Decimal('0.0')}

        super().__init__(name, **kwargs)

    @property
    def is_empty(self):
        return self._value['amount'] == _Decimal('0.0')

    def _on_get(self, value: dict, **kwargs) -> dict:
        return {
            'currency': value['currency'],
            'amount': _Decimal(value['amount']),
        }

    def _on_set(self, value: dict, **kwargs):
        """Set value for the field.
        """
        if value is None:
            return {
                'currency': _currency.get_main(),
                'amount': 0.0,
            }

        # Convert to mutable dict if necessary
        if isinstance(value, _frozendict):
            value = dict(value)

        # Check value type
        if not isinstance(value, dict):
            raise TypeError("Value of the field '{}' should be a dict.".format(self._name))

        # Check for required dict keys
        if 'currency' not in value or not value['currency']:
            raise ValueError("Value of the field '{}' must contain 'currency' key.".format(self._name))
        if 'amount' not in value:
            raise ValueError("Value of the field '{}' must contain 'amount' key.".format(self._name))

        # Check for currency validness
        if value['currency'] not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value['currency']))

        # Float amount should be converted to string before converting to Decimal
        if isinstance(value['amount'], float):
            value['amount'] = str(value['amount'])

        # Convert amount to Decimal
        if not isinstance(value['amount'], float):
            value['amount'] = float(value['amount'])

        return value

    def _on_get_jsonable(self, raw_value: dict, **kwargs):
        raw_value.update({
            'amount': raw_value['amount'],
            'currency_symbol': _currency.get_symbol(raw_value['currency']),
            'currency_title': _currency.get_title(raw_value['currency']),
            'currency_short_title': _currency.get_title(raw_value['currency'], True),
        })

        return raw_value
