# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('recipient_name', models.CharField(verbose_name='收件人', max_length=20)),
                ('recipient_addr', models.CharField(verbose_name='收件地址', max_length=256)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=6)),
                ('recipient_phone', models.CharField(verbose_name='联系电话', max_length=11)),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('username', models.CharField(unique=True, verbose_name='用户名称', max_length=20)),
                ('password', models.CharField(verbose_name='用户密码', max_length=40)),
                ('email', models.EmailField(verbose_name='用户邮箱', max_length=254)),
                ('is_active', models.BooleanField(default=False, verbose_name='激活状态')),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='passport',
            field=models.ForeignKey(verbose_name='账户', to='users.Passport'),
        ),
    ]
