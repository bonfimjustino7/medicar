# Generated by Django 3.0.6 on 2020-05-30 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('crm', models.CharField(max_length=6)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefone', models.CharField(blank=True, max_length=9, null=True)),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Especialidade')),
            ],
        ),
    ]
