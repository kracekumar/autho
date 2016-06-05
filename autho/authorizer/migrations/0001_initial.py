# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 09:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_internal', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Application')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_internal', models.BooleanField()),
                ('can_create', models.BooleanField()),
                ('can_read', models.BooleanField()),
                ('can_edit', models.BooleanField()),
                ('can_delete', models.BooleanField()),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Permissions')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Role')),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.OrganizationUser')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Role')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorizer.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('name', 'organization')]),
        ),
    ]