from django.contrib import admin

from .models import Question, Answer


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    raw_id_fields = ('user',)
    list_display = ['__str__', 'user', 'created_on', 'modified_on']
    exclude = ('created_by', 'modified_by')


class AnswerAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    raw_id_fields = ('user', 'question')
    list_display = ['__str__', 'user', 'created_on', 'modified_on']
    exclude = ('created_by', 'modified_by')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
