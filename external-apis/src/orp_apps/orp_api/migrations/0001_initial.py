# Generated by Django 3.2.7 on 2021-09-13 15:14

# Third Party
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('related_categories', models.ManyToManyField(to='orp_api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('categories', models.ManyToManyField(to='orp_api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('related_documents', models.ManyToManyField(to='orp_api.Document')),
                ('related_entities', models.ManyToManyField(to='orp_api.Entity')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='related_documents',
            field=models.ManyToManyField(to='orp_api.Document'),
        ),
    ]
