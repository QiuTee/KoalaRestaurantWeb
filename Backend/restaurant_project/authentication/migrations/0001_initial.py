# Generated by Django 3.2.8 on 2024-12-13 10:28

import authentication.manager
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('is_verified', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('auth_provider', models.CharField(default='email', max_length=50)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.baseuser')),
                ('phone_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(99999999999)])),
                ('customer_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('join_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.baseuser',),
            managers=[
                ('objects', authentication.manager.CustomerManager()),
            ],
        ),
        migrations.CreateModel(
            name='ManagerAccount',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.baseuser')),
                ('manager_fullname', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('start_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.baseuser',),
            managers=[
                ('objects', authentication.manager.UserManager()),
            ],
        ),
    ]