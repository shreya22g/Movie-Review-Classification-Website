# Generated by Django 3.2.9 on 2021-11-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20211129_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='movie_name',
            field=models.CharField(default=0, max_length=122, verbose_name='name'),
            preserve_default=False,
        ),
    ]
