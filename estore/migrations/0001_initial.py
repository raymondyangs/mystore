# Generated by Django 2.1.3 on 2018-12-16 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='產品名稱')),
                ('description', models.TextField(verbose_name='產品敘述')),
                ('quantity', models.IntegerField(verbose_name='庫存數量')),
                ('price', models.IntegerField(verbose_name='價格')),
            ],
        ),
    ]
