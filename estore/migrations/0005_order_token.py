# Generated by Django 2.1.7 on 2019-02-16 04:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0004_auto_20190216_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='token',
            field=models.UUIDField(db_index=True, default=uuid.uuid4),
        ),
    ]
