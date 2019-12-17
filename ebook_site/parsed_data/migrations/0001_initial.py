# Generated by Django 3.0 on 2019-12-17 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EbookData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='EventData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('date', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('eType', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsed_data.EbookData')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parsed_data.EventData')),
            ],
        ),
        migrations.AddField(
            model_name='ebookdata',
            name='events',
            field=models.ManyToManyField(blank=True, through='parsed_data.EventLog', to='parsed_data.EventData'),
        ),
    ]
