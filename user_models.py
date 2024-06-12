import models as models
from base_types import IntegerField, VarcharField
from pathlib import Path
import sys

PATH = Path(__file__).absolute().parent.parent
sys.path.append(str(PATH))


@models.simple_orm
class Defect(models.Model):
    code = IntegerField()
    defect = VarcharField()
    job_title = VarcharField()
    unit = VarcharField()
    count = IntegerField()


@models.simple_orm
class Employee(models.Model):
    telegram_id = IntegerField()
    first_name = VarcharField()
    second_name = VarcharField()
    surname = VarcharField()
    mail_count = IntegerField()


d = Defect.objects.add(Defect(1, "defect", "job", "unit", 1))
e = Employee.objects.add(Employee(1, "first name", "second name", "surname", 1))
Defect.objects.get(code=1)
Defect.objects.delete(code=1)
print("Работает")
