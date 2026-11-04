from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_weather_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="travelpreference",
            name="budget_level",
        ),
    ]
