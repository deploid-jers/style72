from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields
from tortoise.indexes import Index

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Admin',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('username', fields.CharField(unique=True, max_length=255)),
                ('password_hash', fields.TextField(unique=False)),
                ('full_name', fields.TextField(unique=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'admins', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Category',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('is_active', fields.BooleanField(default=True)),
            ],
            options={'table': 'categories', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Service',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('category', fields.ForeignKeyField('models.Category', source_field='category_id', db_constraint=True, to_field='id', related_name='services', on_delete=OnDelete.CASCADE)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.TextField(null=True, unique=False)),
                ('duration_minutes', fields.IntField()),
                ('price', fields.DecimalField(max_digits=10, decimal_places=2)),
                ('is_active', fields.BooleanField(default=True)),
            ],
            options={'table': 'services', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Specialist',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('full_name', fields.CharField(max_length=255)),
                ('specialization', fields.CharField(max_length=255)),
                ('bio', fields.TextField(null=True, unique=False)),
                ('photo_url', fields.TextField(null=True, unique=False)),
                ('is_active', fields.BooleanField(default=True)),
                ('services', fields.ManyToManyField('models.Service', unique=True, db_constraint=True, through='specialist_services', forward_key='service_id', backward_key='specialists_id', related_name='specialists', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'specialists', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Appointment',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('type', fields.CharField(max_length=20)),
                ('client_name', fields.CharField(max_length=255)),
                ('client_phone', fields.CharField(max_length=50)),
                ('client_comment', fields.TextField(null=True, unique=False)),
                ('specialist', fields.ForeignKeyField('models.Specialist', source_field='specialist_id', null=True, db_constraint=True, to_field='id', related_name='appointments', on_delete=OnDelete.SET_NULL)),
                ('service', fields.ForeignKeyField('models.Service', source_field='service_id', null=True, db_constraint=True, to_field='id', related_name='appointments', on_delete=OnDelete.SET_NULL)),
                ('appointment_date', fields.DateField(null=True)),
                ('appointment_time', fields.TimeField(null=True, auto_now=False, auto_now_add=False)),
                ('status', fields.CharField(default='new', max_length=20)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'appointments', 'app': 'models', 'indexes': [Index(fields=['appointment_date', 'appointment_time']), Index(fields=['status'])], 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='SpecialistSchedule',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('specialist', fields.ForeignKeyField('models.Specialist', source_field='specialist_id', db_constraint=True, to_field='id', related_name='schedules', on_delete=OnDelete.CASCADE)),
                ('work_date', fields.DateField()),
                ('start_time', fields.TimeField(auto_now=False, auto_now_add=False)),
                ('end_time', fields.TimeField(auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'specialist_schedules', 'app': 'models', 'unique_together': (('specialist', 'work_date'),), 'indexes': [Index(fields=['work_date'])], 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
