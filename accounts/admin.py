from django.contrib import admin
from .models import Company, Truck, Producer, Loading


admin.site.register(Loading)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'cnpj', 'user', 'profile_picture')
    list_display = ['id', '__str__', 'name']


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    fields = ('company', 'cnpj')
    list_display = ['__str__', 'company']


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    fields = ('license_plate', 'producer')
    list_display = ['__str__', 'producer']
