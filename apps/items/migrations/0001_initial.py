# Generated by Django 4.2.4 on 2024-09-30 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('observation', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('STARTED', 'Started'), ('COMPLETED', 'Completed'), ('ERROR', 'Error')], default='CREATED', max_length=50)),
                ('robot_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='robots.robot')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
    ]
