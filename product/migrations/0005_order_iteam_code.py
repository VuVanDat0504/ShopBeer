# Generated by Django 2.2.5 on 2020-07-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_beer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='iteam_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
