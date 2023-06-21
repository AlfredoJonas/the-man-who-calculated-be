# Generated by Django 3.2.19 on 2023-06-20 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(help_text='Email to identify the user', max_length=254, unique=True)),
                ('password', models.CharField(help_text='Encoded password', max_length=128)),
                ('status', models.CharField(choices=[('ACTIVE', 'active'), ('INACTIVE', 'inactive')], default='active', help_text='Let us know if the user was disabled/deleted or it is active', max_length=30)),
                ('last_login', models.DateTimeField(help_text='Last time the user do login', null=True)),
            ],
        ),
    ]