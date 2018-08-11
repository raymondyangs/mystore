# Generated by Django 2.1 on 2018-08-06 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0005_order_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='', max_length=255),
        ),
    ]
