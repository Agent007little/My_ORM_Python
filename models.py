import psycopg2  # Необходимо импортировать библиотеку для работы с postgres
import copy
from base_types import IntegerField, VarcharField

db_name = "orm_postgres"  # необходимо создать нужную базу данных перед подключением к ней.

BASIC_TYPES = [IntegerField, VarcharField]
EXTERN_TYPES = {}


def simple_orm(class_: type):
    EXTERN_TYPES[class_.__name__] = class_
    class_.objects.__createTable__()

    return class_


class ListOfObjects:
    def __init__(self, objects):
        self.objects = objects

    def filter(self, **kwargs):
        filtered_objects = []
        for obj in self.objects:
            # Check if all specified attributes and their values match
            if all(getattr(obj, attr, None) == value for attr, value in kwargs.items()):
                filtered_objects.append(obj)
        return ListOfObjects(filtered_objects)

    def delete(self):
        for obj in self.objects:
            obj.delete()

    def json(self):
        object_dicts = [obj.json() for obj in self.objects]
        return object_dicts


class ProxyObjects:
    def __get__(self, instance, owner):
        return Object(owner)


class Model:
    objects = ProxyObjects()

    def __init__(self, *args, **kwargs):
        fields = [el for el in vars(self.__class__) if not el.startswith("__")]  # поля, которые мы создали в модели
        for i, value in enumerate(args):
            setattr(self, fields[i], value)  # задаем переменные переданные с помощью args

        for field, value in kwargs.items():  # задаем переменные переданные с помощью kwargs
            setattr(self, field, value)


class Object:
    def __init__(self, object_type: type):
        # Конструктор класса принимает тип объекта (класс) и сохраняет его в атрибуте object_type.
        self.object_type = object_type

    def add(self, obj):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        d = copy.copy(obj.__dict__)

        object_type_name = self.object_type.__name__

        insert_sql = f'INSERT INTO {object_type_name} ({", ".join(obj.__dict__.keys())}) VALUES ' \
                     f'({", ".join(["%s"] * len(obj.__dict__))});'

        values = tuple(d.values())
        cursor.execute(insert_sql, values)
        conn.commit()
        conn.close()
        return obj

    def save(self, obj):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        d = copy.copy(obj.__dict__)

        object_type_name = self.object_type.__name__

        upsert_sql = f'INSERT OR REPLACE INTO {object_type_name} ({", ".join(obj.__dict__.keys())}) VALUES ' \
                     f'({", ".join(["%s"] * len(obj.__dict__))});'

        values = tuple(d.values())
        cursor.execute(upsert_sql, values)
        conn.commit()
        conn.close()
        return obj

    def get(self, **kwargs):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = %s' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        select_by_attrs_sql = f'SELECT * FROM {object_type_name} WHERE {where_clause};'

        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(select_by_attrs_sql, values)
        row = cursor.fetchone()
        conn.close()

        if row:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)

            return obj
        else:
            return None

    def delete(self, **kwargs):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = %s' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        delete_by_attrs_sql = f'DELETE FROM {object_type_name} WHERE {where_clause};'
        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(delete_by_attrs_sql, values)
        conn.commit()
        conn.close()

    def filter(self, **kwargs):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__

        attr_value_pairs = [(attr, value) for attr, value in kwargs.items()]

        where_clauses = [f'{attr} = %s' for attr, _ in attr_value_pairs]
        where_clause = ' AND '.join(where_clauses)
        select_by_attrs_sql = f'SELECT * FROM {object_type_name} WHERE {where_clause};'

        values = tuple(value for _, value in attr_value_pairs)

        cursor.execute(select_by_attrs_sql, values)
        rows = cursor.fetchall()
        conn.close()

        objects = []
        for row in rows:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)

            objects.append(obj)

        return objects

    def all(self):
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
        )
        cursor = conn.cursor()

        object_type_name = self.object_type.__name__
        select_all_sql = f'SELECT * FROM {object_type_name};'

        cursor.execute(select_all_sql)
        rows = cursor.fetchall()
        conn.close()

        objects = []
        for row in rows:
            obj = self.object_type()
            for i, value in enumerate(row):
                setattr(obj, cursor.description[i][0], value)
            objects.append(obj)

        return objects

    def __createTable__(self):
        # Метод для создания таблицы в базе данных, основанной на атрибутах класса object_type.

        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            host='postgres',
            user='postgres',
            password='12345',
            database=db_name,
            port="5432"
            )
        cursor = conn.cursor()

        # Создаём список custom_fields для хранения определений полей таблицы.
        custom_fields = []

        # Проходимся по атрибутам класса object_type и извлекаем информацию о полях.
        for key, value in vars(self.object_type).items():
            if not key.startswith("__") and not callable(value):
                field_name = key
                field_type = value.field_type
                is_unique = value.unique
                is_null = value.null
                default_value = value.default

                # Создаём строку с определением поля и добавляем её в список custom_fields.
                field_declaration = [f'"{field_name}" {field_type}']

                if is_unique:
                    field_declaration.append('UNIQUE')
                if not is_null:
                    field_declaration.append('NOT NULL')
                if default_value is not None:
                    field_declaration.append(f'DEFAULT {default_value}')

                custom_fields.append(' '.join(field_declaration))

        # Создаём SQL-запрос для создания таблицы с определёнными полями.
        create_table_sql = f'''CREATE TABLE IF NOT EXISTS {self.object_type.__name__} ( id SERIAL PRIMARY KEY, 
        {", ".join(custom_fields)});'''

        # Выполняем SQL-запрос.
        cursor.execute(create_table_sql)

        # Фиксируем изменения и закрываем соединение с базой данных.
        conn.commit()
        conn.close()
