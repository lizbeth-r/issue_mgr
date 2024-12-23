# Generated by Django 5.1.2 on 2024-11-02 17:37

from django.db import migrations

def populate_team(apps, schemaeditor):
    entries = {
        "alpha": "The A team",
        "bravo": "The B team",
        "charlie": "The C team"
    }
    Team = apps.get_model("accounts", "Team")
    for key, value in entries.items():
        team = Team(name=key, description=value)
        team.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20241102_1737'),
    ]

    operations = [
        migrations.RunPython(populate_team)
    ]
