from .helpers import unpack, snake_case, del_by_value, del_keys, rename_keys
import decimal


class Payment:
    def __init__(self, payment):
        self.status, self.value = unpack(payment, 'PaymentDetails')

        self._map()

    def _map(self):
        _del_keys = ['comment',
                     'person_date_of_birth',
                     'person_first_name',
                     'person_gender_id',
                     'person_last_name',
                     'first_name',
                     'last_name',
                     'bank_account',
                     'bank_account_id',
                     'fa_date_time',
                     # 'kid', keep!
                     'status',
                     'receiver']

        # renamed, original
        keys = [('id', 'payment_id'),
                ('method_id', 'payment_method_id'),
                ('receiver', 'payment_receiver'),
                ('receiver_org_id', 'payment_receiver_org_id'),
                ('person_id', 'relation_id_customer'),
                ('person_type', 'relation_type_id_customer'),
                ('org_id', 'product_type')  # Hackish for 376 in NIF
                ]

        self.value = snake_case(self.value)
        self.value = del_by_value(self.value, None)
        self.value = del_keys(self.value, _del_keys)
        self.value = rename_keys(self.value, keys)

        for k, v in self.value.items():
            if isinstance(v, decimal.Decimal) is True:
                self.value[k] = float(v)
