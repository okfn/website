# Generated by Django 3.2.16 on 2023-06-02 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='PillButton',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='pill_button_pillbutton', serialize=False, to='cms.cmsplugin')),
                ('text', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('another_window', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]