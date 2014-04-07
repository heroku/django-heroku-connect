from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models

class SalesforceReferenceField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'max_length': 18,
            'null': True,
            'blank': True,
        })
        super(SalesforceReferenceField, self).__init__(*args, **kwargs)


class SalesforceBase(models.Model):
    class Meta:
        abstract = True

    # SF Reserved columns
    sfid = SalesforceReferenceField()
    is_deleted = models.NullBooleanField(db_column='isdeleted')
    system_mod_stamp = models.DateTimeField(db_column='systemmodstamp',
        null=True, blank=True)

    # Timestamps & related references
    created_by_id = SalesforceReferenceField(db_column='createdbyid')
    created_date = models.DateTimeField(db_column='createddate', null=True,
        blank=True)
    last_modified_by_id = SalesforceReferenceField(db_column='lastmodifiedbyid')
    last_modified_date = models.DateTimeField(db_column='lastmodifieddate',
        null=True, blank=True)
    last_activity_date = models.DateField(db_column='lastactivitydate',
        null=True, blank=True)
    last_referenced_date = models.DateTimeField(db_column='lastreferenceddate',
        null=True, blank=True)
    last_viewed_date = models.DateTimeField(db_column='lastvieweddate',
        null=True, blank=True)

    # Other references
    master_record_id = SalesforceReferenceField(db_column='masterrecordid')
    owner_id = SalesforceReferenceField(db_column='ownerid')

def add_address_fields(model_class, prefixes):
    fields = (
        ('street', models.CharField, {
            'max_length': 255,
            'null': True,
            'blank': True,
        }),
        ('city', models.CharField, {
            'max_length': 40,
            'null': True,
            'blank': True,
        }),
        ('state', models.CharField, {
            'max_length': 80,
            'null': True,
            'blank': True,
        }),
        ('state_code', models.CharField, {
            'max_length': 10,
            'null': True,
            'blank': True,
        }),
        ('postal_code', models.CharField, {
            'max_length': 20,
            'null': True,
            'blank': True,
        }),
        ('country', models.CharField, {
            'max_length': 80,
            'null': True,
            'blank': True,
        }),
        ('country_code', models.CharField, {
            'max_length': 10,
            'null': True,
            'blank': True,
        }),
        ('latitude', models.FloatField, {'null': True, 'blank': True}),
        ('longitude', models.FloatField, {'null': True, 'blank': True}),
    )

    for prefix in prefixes:
        for suffix, field_type, field_kwargs in fields:
            field_name = '_'.join((prefix, suffix))
            db_column = field_name.replace('_', '')
            model_class.add_to_class(field_name, field_type(db_column=db_column,
                **field_kwargs))


class Account(SalesforceBase):
    class Meta:
        db_table = '"{0}"."account"'.format(settings.HEROKU_CONNECT_SCHEMA)

    def __unicode__(self):
        return 'Account: {0}'.format(self.name)

    salesforce_object_name = 'Account'

    # References
    parent_id = SalesforceReferenceField(db_column='parentid')
    jigsaw_company_id = models.CharField(db_column='jigsawcompanyid',
        max_length=20, null=True, blank=True)

    # General info
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    account_type = models.CharField(db_column='type', max_length=40, null=True,
        blank=True)
    account_number = models.CharField(db_column='accountnumber', max_length=40,
        null=True, blank=True)
    industry = models.CharField(max_length=40, null=True, blank=True)
    number_of_employees = models.IntegerField(db_column='numberofemployees',
        null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
add_address_fields(Account, ('shipping', 'billing'))

class Contact(SalesforceBase):
    class Meta:
        db_table = '"{0}"."contact"'.format(settings.HEROKU_CONNECT_SCHEMA)

    def __unicode__(self):
        return 'Contact: {0}'.foramt(self.name)

    salesforce_object_name = 'Contact'

    # References
    jigsaw_contact_id = models.CharField(db_column='jigsawcontactid',
        max_length=20, null=True, blank=True)
    jigsaw = models.CharField(max_length=20, null=True, blank=True)
    reports_to_id = SalesforceReferenceField(db_column='reportstoid')
    account_id = SalesforceReferenceField(db_column='accountid')

    # General info
    name = models.CharField(max_length=255, null=True, blank=True)
    salutation = models.CharField(max_length=40, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=80, null=True, blank=True)

    assistant_name = models.CharField(db_column='assistantname', max_length=40,
        null=True, blank=True)
    assistant_phone = models.CharField(db_column='assistantphone',
        max_length=40, null=True, blank=True)

    lead_source = models.CharField(db_column='leadsource', max_length=40,
        null=True, blank=True)
    last_cu_update_date = models.DateTimeField(db_column='lastcuupdatedate',
        null=True, blank=True)
    last_cu_request_date = models.DateTimeField(db_column='lastcurequestdate',
        null=True, blank=True)

    # Email
    email = models.CharField(max_length=80, null=True, blank=True)
    email_bounced_date = models.DateTimeField(db_column='emailbounceddate',
        null=True, blank=True)
    email_bounced_reason = models.CharField(db_column='emailbouncedreason',
        max_length=255, null=True, blank=True)
    is_email_bounced = models.NullBooleanField(db_column='isemailbounced')
    has_opted_out_of_email = models.NullBooleanField(
        db_column='hasoptedoutofemail')

    # Phones (SO MANY PHONES)
    phone = models.CharField(max_length=40, null=True, blank=True)
    fax = models.CharField(max_length=40, null=True, blank=True)
    home_phone = models.CharField(db_column='homephone', max_length=40,
        null=True, blank=True)
    mobile_phone = models.CharField(db_column='mobilephone', max_length=40,
        null=True, blank=True)
    other_phone = models.CharField(db_column='otherphone', max_length=40,
        null=True, blank=True)
    has_opted_out_of_fax = models.NullBooleanField(db_column='hasoptedoutoffax')
    do_not_call = models.NullBooleanField(db_column='donotcall')
add_address_fields(Contact, ('mailing', 'other'))
