# Generated by Django 2.0.5 on 2018-07-06 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180621_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='catalog.Language'),
        ),
    ]
