from django.contrib         import admin
from django.core.exceptions import ValidationError
from .models                import Client 


class ClientAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e.message)

admin.site.register(Client, ClientAdmin)