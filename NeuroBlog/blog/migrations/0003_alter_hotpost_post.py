# Generated by Django 3.2.15 on 2022-12-25 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_hotposts_hotpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', unique=True),
        ),
    ]
