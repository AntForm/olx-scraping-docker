# Generated by Django 2.2 on 2019-06-17 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OlxLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olx.OlxRequest')),
            ],
        ),
    ]