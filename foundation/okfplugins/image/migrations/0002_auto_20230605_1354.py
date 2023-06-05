# Generated by Django 3.2.16 on 2023-06-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='okimage',
            name='in_column',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='alt',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='more_text',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='tag',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='text',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='okimage',
            name='url',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]