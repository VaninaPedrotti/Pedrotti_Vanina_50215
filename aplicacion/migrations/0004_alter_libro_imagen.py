# Generated by Django 5.0.2 on 2024-03-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_alter_libro_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='imagen',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='libros/'),
        ),
    ]
