# Generated by Django 3.2.15 on 2023-01-13 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_order_with_respect_to'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='post',
            order_with_respect_to=None,
        ),
    ]
