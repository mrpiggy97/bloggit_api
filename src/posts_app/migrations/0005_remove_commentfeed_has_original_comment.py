# Generated by Django 2.2.4 on 2019-10-29 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0004_auto_20191029_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentfeed',
            name='has_original_comment',
        ),
    ]
