# Generated by Django 2.2.4 on 2019-10-29 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0003_commentfeed_has_original_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfeed',
            name='has_original_comment',
            field=models.BooleanField(default=False),
        ),
    ]
