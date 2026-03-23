import csv
from django.http import HttpResponse
from django.apps import AppConfig


class MyauthConfig(AppConfig):
    name = 'myauth'


class ExportAsCSVMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # 1. Явно указываем нужные поля (без паролей и лишней служебной инфы)
        field_names = ['email', 'name', 'last_name', 'dni', 'birthdate', 'is_student', 'is_tutor', 'group']

        response = HttpResponse(content_type='text/csv')
        # Имя файла будет например "user_export.csv"
        response['Content-Disposition'] = f'attachment; filename={meta.model_name}_export.csv'

        writer = csv.writer(response)
        # Записываем заголовки
        writer.writerow(field_names)

        # 2. Записываем данные
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)

                # Если это ForeignKey (группа), выгружаем её строковое представление
                if field == 'group' and value:
                    value = str(value)

                row.append(value)
            writer.writerow(row)

        return response

    # 3. Описание для интерфейса админки
    export_as_csv.short_description = "Exportar seleccionados a CSV"

    # Добавляем действие в выпадающий список "Action" в админке
    export_as_csv.short_description = "Экспортировать выбранные в CSV"
