# Generated by Django 4.2.7 on 2024-01-15 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0011_alter_usermy_packed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermy',
            name='packed',
            field=models.ForeignKey(default='normal paket', on_delete=django.db.models.deletion.CASCADE, to='appUser.packed', verbose_name='Pakedi'),
        ),
    ]
