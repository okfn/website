# Generated by Django 4.2.3 on 2024-06-11 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0024_remove_unitmembership_person_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardmembership',
            name='board',
        ),
        migrations.RemoveField(
            model_name='boardmembership',
            name='person',
        ),
        migrations.DeleteModel(
            name='Board',
        ),
        migrations.DeleteModel(
            name='BoardMembership',
        ),
    ]