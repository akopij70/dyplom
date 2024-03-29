# Generated by Django 4.2.5 on 2023-09-16 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('release_date', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, default='movies_thumbnails/logo.jpg', null=True, upload_to='movies_thumbnails')),
            ],
            options={
                'verbose_name_plural': 'Nasze filmy',
                'ordering': ('title',),
            },
        ),
    ]
