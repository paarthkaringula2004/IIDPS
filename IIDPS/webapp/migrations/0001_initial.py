# Generated by Django 2.2.4 on 2022-02-08 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usertab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_a_m_e', models.CharField(max_length=149)),
                ('e_mail', models.CharField(max_length=149)),
                ('pass_word', models.CharField(max_length=149)),
                ('phone', models.CharField(max_length=149)),
                ('gender', models.CharField(max_length=149)),
                ('picture', models.CharField(max_length=149)),
            ],
        ),
    ]
