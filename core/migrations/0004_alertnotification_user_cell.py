# Generated by Django 5.0.6 on 2024-06-12 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_networktraffic_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol_type', models.CharField(max_length=10)),
                ('service', models.CharField(max_length=50)),
                ('email', models.BooleanField(default=True)),
                ('sms', models.BooleanField(default=True)),
                ('outcome', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='cell',
            field=models.CharField(default='+263776149765', max_length=20),
        ),
    ]
