# Generated by Django 3.1.3 on 2020-11-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_Blog', '0003_auto_20201105_1931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
