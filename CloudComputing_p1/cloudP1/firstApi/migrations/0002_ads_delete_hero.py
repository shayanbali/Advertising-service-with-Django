# Generated by Django 4.1.3 on 2022-11-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=400)),
                ('email', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, default='pending', max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Hero',
        ),
    ]
