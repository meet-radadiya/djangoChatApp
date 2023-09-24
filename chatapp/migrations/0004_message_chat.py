# Generated by Django 4.2.5 on 2023-09-24 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_remove_message_recipient_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='chatapp.chat'),
            preserve_default=False,
        ),
    ]