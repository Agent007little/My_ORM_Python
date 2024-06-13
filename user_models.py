import models as models
from base_types import IntegerField, VarcharField


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



