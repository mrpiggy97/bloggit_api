# Generated by Django 2.2.4 on 2019-10-28 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0002_comment_commentfeed'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentfeed',
            name='has_original_comment',
            field=models.BooleanField(default=True),
        ),
    ]
