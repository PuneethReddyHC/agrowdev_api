# Generated by Django 2.2.10 on 2020-03-07 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('postbaseinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='material.PostBaseInfo')),
                ('directors', models.CharField(blank=True, help_text='director', max_length=255, null=True, verbose_name='director')),
                ('actors', models.CharField(blank=True, help_text='actor', max_length=255, null=True, verbose_name='actor')),
                ('region', models.CharField(blank=True, help_text='region', max_length=20, null=True, verbose_name='region')),
                ('language', models.CharField(blank=True, help_text='language', max_length=20, null=True, verbose_name='language')),
                ('length', models.IntegerField(blank=True, default=0, help_text='Duration', null=True, verbose_name='Duration')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movielist',
            },
            bases=('material.postbaseinfo',),
        ),
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('CN', 'Chinese'), ('EN', 'English')], help_text='two language categories are now available', max_length=5, null=True, verbose_name='article details language category')),
                ('origin_content', models.TextField(help_text='original content', verbose_name='original content')),
                ('formatted_content', models.TextField(help_text='processed content', verbose_name='processed content')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='Add Time', null=True, verbose_name='Add Time')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='modification time', null=True, verbose_name='modification time')),
                ('movie_info', models.ForeignKey(blank=True, help_text='content', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='movie.MovieInfo', verbose_name='content')),
            ],
            options={
                'verbose_name': 'Movie Details',
                'verbose_name_plural': 'Movie Detailslist',
            },
        ),
    ]