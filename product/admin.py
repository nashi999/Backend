from django.contrib import admin
from product.models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','carbonEmission', 'weight', 'company', 'last_update')
    
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id','product','material','quantity','carbonEmission')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name','carbonEmission', 'unit')
    
@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ('id','name','carbonEmission')

@admin.register(LogT)
class LogTAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'distance', 'transportation','carbonEmission','timestamp')

@admin.register(LogI)
class LogIAdmin(admin.ModelAdmin):
    list_display = ('id','user','logType', 'product','amount','carbonEmission','timestamp')
    
admin.site.register(AbstractLog)


admin.site.register(Tag)
admin.site.register(UploadMaterial)
