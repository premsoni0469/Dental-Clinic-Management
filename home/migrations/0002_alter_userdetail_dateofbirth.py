# Generated by Django 5.0.3 on 2024-03-14 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='dateofbirth',
            field=models.CharField(max_length=200),
        ),
    ]
