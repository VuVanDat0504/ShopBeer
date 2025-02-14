# Generated by Django 2.2.5 on 2020-07-11 17:23

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('category', models.CharField(max_length=256)),
                ('picture', models.ImageField(null=True, upload_to=product.models.beer_directory_path)),
            ],
            options={
                'db_table': 'product_beer',
            },
        ),
    ]
