# Generated by Django 4.0.3 on 2022-03-16 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0003_remove_author_created_by_remove_publisher_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
