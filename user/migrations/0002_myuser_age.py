# Generated by Django 2.2.5 on 2020-07-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='age',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
