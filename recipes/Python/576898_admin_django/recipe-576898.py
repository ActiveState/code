from django.contrib import admin
from cadastro_os.models import *

class DesenvolveInline(admin.TabularInline):
    model = Desenvolve
    extra = 1

class OSAdmin(admin.ModelAdmin):
    inlines= (DesenvolveInline,)

class DesenvolveAdmin(admin.ModelAdmin):
    list_display = ('func_id','os_id')

admin.site.register(Projeto)
admin.site.register(Funcionario,OSAdmin)
admin.site.register(Membro)
admin.site.register(Andamento)
admin.site.register(OS,OSAdmin)
admin.site.register(Desenvolve,DesenvolveAdmin)
