# Generated by Django 5.0.2 on 2024-03-26 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0005_alter_libro_options_libro_ubicacion_comentario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='comentario',
            new_name='objeto_comentado',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='nombre',
            new_name='usuario',
        ),
    ]