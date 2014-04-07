from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text

from .tests.factories import AccountFactory, ContactFactory
from .models import Account, Contact

class ConnectModelAdmin(admin.ModelAdmin):
    list_display = (
        'sfid',
        'name',
        'is_deleted',
        'last_modified_date',
    )
    actions = (
        'generate_new_action',
    )
    change_list_template = 'connect_client/admin/change_list.html'

    def factory(self):
        raise NotImplementedError('Subclasses must implement this.')

    def admin_url(self, url_name):
        return urlresolvers.reverse(admin_urlname(self.opts, url_name))

    def generate_new_view(self, request):
        plural_name = force_text(self.opts.verbose_name_plural)
        if request.method == 'POST':
            num = int(request.POST['num'])
            for i in range(num):
                self.factory()
            self.message_user(request, 'Created {0} {1}.'.format(num,
                plural_name), messages.SUCCESS)
            return HttpResponseRedirect(self.admin_url('changelist'))
        else:
            context = dict(
                #self.admin_site.each_context(),
                title='Generate New {0}'.format(plural_name.capitalize()),
                opts=self.opts,
            )
            return TemplateResponse(request,
                'connect_client/admin/generate_new.html', context)

    def get_urls(self):
        urls = super(ConnectModelAdmin, self).get_urls()
        return patterns('',
            url(r'^generate_new/$', self.generate_new_view,
                name="connect_client_{0}_generate_new".format(
                    self.opts.module_name)),
        ) + urls


class AccountAdmin(ConnectModelAdmin):
    factory = AccountFactory


class ContactAdmin(ConnectModelAdmin):
    factory = ContactFactory


admin.site.register(Account, AccountAdmin)
admin.site.register(Contact, ContactAdmin)
