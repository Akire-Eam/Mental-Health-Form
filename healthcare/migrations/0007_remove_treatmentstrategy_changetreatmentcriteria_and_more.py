# Generated by Django 4.0.1 on 2024-06-11 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0006_rename_agression_counselling_aggression'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='changeTreatmentCriteria',
        ),
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='clientConcurred',
        ),
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='patientId',
        ),
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='sessionsPerMonth',
        ),
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='treatmentCriteria',
        ),
        migrations.RemoveField(
            model_name='treatmentstrategy',
            name='treatmentRemarks',
        ),
        migrations.AddField(
            model_name='treatmentplan',
            name='approaches',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatmentplan',
            name='personalResponsibilities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatmentplan',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatmentplan',
            name='specificProblem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatmentplan',
            name='timeFrame',
            field=models.TextField(blank=True, null=True),
        ),
    ]
