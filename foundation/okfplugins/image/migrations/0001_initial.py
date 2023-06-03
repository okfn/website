# Generated by Django 3.2.16 on 2023-06-03 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='OKImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='image_okimage', serialize=False, to='cms.cmsplugin')),
                ('tag', models.CharField(max_length=200)),
                ('image_url', models.ImageField(upload_to='video/images')),
                ('text', models.CharField(default='', max_length=400)),
                ('more_text', models.CharField(default='', max_length=400)),
                ('url', models.CharField(default='', max_length=400)),
                ('caption', models.CharField(default='', max_length=400)),
                ('alt', models.CharField(default='', max_length=400)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
