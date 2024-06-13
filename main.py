from deserializer import deserializer
from user_models import Defect, Employee

raw_json_defect = '{"Defect": {"code": 4, "defect": "defect", "job_title": "job", "unit": "unit", "count": 4}}'
raw_json_employee = '{"Employee": {"telegram_id": 3, "first_name": "first_name", "second_name": "second_name",' \
                    ' "surname": "surname", "mail_count": 3}}'
# Ниже операции создания, изменения и удаления данных
Defect.objects.add(Defect(**deserializer(raw_json_defect)))
Employee.objects.add(Employee(**deserializer(raw_json_employee)))
Defect.objects.add(Defect(1, "defect", "job", "unit", 1))
Employee.objects.add(Employee(1, "first name", "second name", "surname", 1))
Defect.objects.delete(code=1)  # Удаление
d = Defect.objects.get(code=4)  # Пример update.
d.defect = 'new_defect'
Defect.objects.save(d)
print("Конец работы")
