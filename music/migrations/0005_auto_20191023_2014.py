# Generated by Django 2.2.6 on 2019-10-23 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20191023_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicpost',
            name='artist_info',
            field=models.CharField(default='/', max_length=100),
        ),
        migrations.AddField(
            model_name='musicpost',
            name='song_info',
            field=models.CharField(default='/', max_length=100),
        ),
        migrations.AlterField(
            model_name='musicpost',
            name='artist_id',
            field=models.CharField(default='AvKjgEoyvDKQ9PoOA', max_length=100),
        ),
        migrations.AlterField(
            model_name='musicpost',
            name='artist_name',
            field=models.CharField(default='ysFKK', max_length=100),
        ),
        migrations.AlterField(
            model_name='musicpost',
            name='artist_terms',
            field=models.CharField(default='IWXWK', max_length=100),
        ),
        migrations.AlterField(
            model_name='musicpost',
            name='song_id',
            field=models.SlugField(default='eTXI3uHTu9jRsCwSM', unique=True),
        ),
    ]
