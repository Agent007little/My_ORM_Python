import json


# Пример получаемого JSON
# data = '{"Defect": {"code": 4, "defect": "defect", "job_title": "job", "unit": "unit", "count": 4}}'
def deserializer(data: json) -> dict:
    # Переводим в python объект
    data = json.loads(data)
    # Получаем имя модели
    key = list(data.keys())[0]
    # Возвращаем только аргументы модели в виде словаря
    return data[key]

# Как вариант через marshmallow или pydantic можно преобразовать json в класс. Но я с этим не до конца разобрался.
# Сделал максимально просто и прямолинейно.
