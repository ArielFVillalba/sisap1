# Generated by Django 4.2.7 on 2023-11-18 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('idarticulo', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.DecimalField(decimal_places=0, max_digits=12)),
                ('descripcion', models.TextField()),
                ('unidad', models.TextField()),
                ('costo', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('iva', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('familia1', models.TextField(blank=True, null=True)),
                ('familia2', models.TextField(blank=True, null=True)),
                ('familia3', models.TextField(blank=True, null=True)),
                ('familia4', models.TextField(blank=True, null=True)),
                ('familia5', models.TextField(blank=True, null=True)),
                ('familia6', models.TextField(blank=True, null=True)),
                ('familia7', models.TextField(blank=True, null=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('muevestock', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'articulos',
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposito', models.TextField(blank=True, null=True)),
                ('sucursal', models.TextField()),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'deposito',
            },
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.DecimalField(decimal_places=0, max_digits=20)),
                ('deposito', models.TextField()),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=20)),
                ('unidad', models.TextField()),
            ],
            options={
                'db_table': 'existencia',
            },
        ),
        migrations.CreateModel(
            name='Movdepcab',
            fields=[
                ('idmovdepcab', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('nromov', models.TextField()),
                ('depsalida', models.TextField()),
                ('depentrada', models.TextField()),
                ('obs', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'movdep_cab',
            },
        ),
        migrations.CreateModel(
            name='Movdepdet',
            fields=[
                ('idmovdepdet', models.AutoField(primary_key=True, serialize=False)),
                ('idmovdepcab', models.DecimalField(decimal_places=0, max_digits=20)),
                ('orden', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('idarticulo', models.DecimalField(decimal_places=0, max_digits=20)),
                ('codigo', models.DecimalField(decimal_places=0, max_digits=12)),
                ('descripcion', models.TextField()),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=12)),
                ('unidad', models.TextField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=20)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('iva', models.DecimalField(decimal_places=0, max_digits=4)),
                ('depsalida', models.TextField()),
                ('depentrada', models.TextField()),
                ('usuario', models.TextField()),
            ],
            options={
                'db_table': 'movdep_det',
            },
        ),
    ]