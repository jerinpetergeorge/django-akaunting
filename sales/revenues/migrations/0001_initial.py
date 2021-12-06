# Generated by Django 3.1.13 on 2021-12-06 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import sales.revenues.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('attachment', models.FileField(blank=True, upload_to=sales.revenues.models._revenue_upload_to, verbose_name='Attachment')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenues', related_query_name='revenue', to='categories.category', verbose_name='Category')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenues', related_query_name='revenue', to='customers.customer', verbose_name='Customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenues', related_query_name='revenue', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Revenue',
                'verbose_name_plural': 'Revenues',
                'db_table': 'Revenues',
            },
        ),
    ]
