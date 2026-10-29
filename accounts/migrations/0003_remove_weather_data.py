from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_travelpreference_budget_level_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="travelpreference",
            name="include_weather",
        ),
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS weather_weathersnapshot",
        ),
    ]
