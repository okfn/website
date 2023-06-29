# Generated by Django 3.2.16 on 2023-06-29 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='list_list', serialize=False, to='cms.cmsplugin')),
                ('title', models.CharField(blank=True, max_length=500)),
                ('items', models.TextField(blank=True)),
                ('list_type', models.CharField(choices=[('long', 'Long'), ('short', 'Short'), ('xl', 'XL')], default='long', max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
