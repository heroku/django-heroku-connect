from __future__ import absolute_import, unicode_literals

import os

from factory import Sequence
from factory.django import DjangoModelFactory
from shams import factory as sham

from .. import models

def address_mixin(prefix):
    fields = (
        ('street', sham.StreetAddress()),
        ('city', sham.Name(min_words=1, max_words=3)),
        ('state', sham.State()),
        ('postal_code', sham.ZipCode()),
        ('country', 'United States'),
    )

    attrs = {}
    for f, s in fields:
        attrs['_'.join((prefix, f))] = s
    attrs['ABSTRACT_FACTORY'] = True
    return type('{0}AddressMixin'.format(prefix.capitalize()).encode('utf-8'),
            (DjangoModelFactory, object), attrs)

ShippingAddressMixin = address_mixin('shipping')
BillingAddressMixin = address_mixin('billing')
MailingAddressMixin = address_mixin('mailing')
OtherAddressMixin = address_mixin('other')


class SalesforceFactory(DjangoModelFactory):
    ABSTRACT_FACTORY = True
    id = sham.Number()


class AccountFactory(BillingAddressMixin, ShippingAddressMixin,
        SalesforceFactory):
    FACTORY_FOR = models.Account

    name = sham.Name()
    description = sham.Blob()
    account_number = sham.UnicodeNumber()
    number_of_employees = sham.Number(min=1, max=10**6)
    phone = sham.Phone()
    website = sham.Url()

class ContactFactory(MailingAddressMixin, OtherAddressMixin,
        SalesforceFactory):
    FACTORY_FOR = models.Contact

    name = sham.Name()
    description = sham.Blob()
    phone = sham.Phone()
