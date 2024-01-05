# Generated by Django 4.2.7 on 2024-01-05 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0003_alter_contents_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='title',
            field=models.CharField(max_length=50, null=True, verbose_name='Başlık'),
        ),
        migrations.AlterField(
            model_name='contents',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appMy.category', verbose_name='Kategori'),
        ),
    ]
