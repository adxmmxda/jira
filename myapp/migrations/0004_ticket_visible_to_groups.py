# Generated by Django 4.2.3 on 2024-06-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_profiles_user_ticket_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='visible_to_groups',
            field=models.CharField(blank=True, help_text='Comma-separated list of group names', max_length=200),
        ),
    ]
