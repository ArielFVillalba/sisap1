# Generated by Django 4.2.7 on 2023-11-18 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='auditoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('accion', models.TextField()),
                ('usuario', models.TextField()),
                ('tabla', models.TextField()),
                ('old', models.JSONField()),
                ('new', models.JSONField()),
            ],
            options={
                'db_table': 'auditoria',
            },
        ),
    ]