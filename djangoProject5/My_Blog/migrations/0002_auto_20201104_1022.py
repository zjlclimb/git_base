# Generated by Django 3.1.3 on 2020-11-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_Blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
