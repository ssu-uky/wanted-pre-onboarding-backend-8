# Generated by Django 4.2.4 on 2023-08-06 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WantedBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=30, verbose_name='제목')),
                ('content', models.TextField(max_length=300, verbose_name='내용')),
                ('job_type', models.CharField(max_length=20)),
                ('Links', models.URLField()),
                ('file', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
