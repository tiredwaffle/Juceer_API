# Generated by Django 2.2.6 on 2019-10-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MusicPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.SlugField(default='fSlKMzdV5CdGNvcv1', unique=True)),
                ('artist_hotttnesss', models.FloatField(default=0)),
                ('artist_id', models.CharField(default='9n8AqIeW8uWNZeqlm', max_length=100)),
                ('artist_name', models.CharField(default='L3G0E', max_length=100)),
                ('artist_terms', models.CharField(default='6x0ge', max_length=100)),
                ('release_id', models.IntegerField(default=0)),
                ('song_hotttnesss', models.FloatField(default=0)),
                ('song_year', models.IntegerField(default=0)),
            ],
        ),
    ]
