from django.apps import apps
from django.contrib import admin


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})


Wishlist = apps.get_model(app_label='wishlist', model_name='Wishlist')
admin.site.register(Wishlist, admin_class)
