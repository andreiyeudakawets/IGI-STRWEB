# Generated by Django 5.0.4 on 2024-04-30 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('gender', models.CharField(help_text='female/male', max_length=6)),
                ('age', models.SmallIntegerField()),
                ('amount_of_feed', models.PositiveIntegerField(help_text='per day (g)')),
                ('countries', models.ManyToManyField(to='animals.country')),
            ],
        ),
    ]
