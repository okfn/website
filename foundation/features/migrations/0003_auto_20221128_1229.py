# Generated by Django 3.2.15 on 2022-11-28 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_remove_feature_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ['order', 'title'], 'verbose_name_plural': 'features'},
        ),
        migrations.AddField(
            model_name='feature',
            name='order',
            field=models.PositiveIntegerField(default=100),
        ),
    ]