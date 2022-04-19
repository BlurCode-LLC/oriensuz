# Generated by Django 3.2.5 on 2022-04-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_auto_20220417_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='sent_to_telegram',
            field=models.BooleanField(default=False, verbose_name='Отправлен в телеграм?'),
        ),
        migrations.AddField(
            model_name='conferencearticle',
            name='sent_to_telegram',
            field=models.BooleanField(default=False, verbose_name='Отправлен в телеграм?'),
        ),
        migrations.AddField(
            model_name='journal',
            name='sent_to_telegram',
            field=models.BooleanField(default=False, verbose_name='Отправлен в телеграм?'),
        ),
        migrations.AddField(
            model_name='journalarticle',
            name='sent_to_telegram',
            field=models.BooleanField(default=False, verbose_name='Отправлен в телеграм?'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='conferencearticle',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='journalarticle',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Slug'),
        ),
    ]