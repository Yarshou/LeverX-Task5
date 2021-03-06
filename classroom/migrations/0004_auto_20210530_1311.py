# Generated by Django 3.2.3 on 2021-05-30 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_auto_20210529_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentary',
            options={'ordering': ['create_date']},
        ),
        migrations.RenameField(
            model_name='lecture',
            old_name='course_id',
            new_name='course',
        ),
        migrations.AlterField(
            model_name='commentary',
            name='mark_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentary', to='classroom.mark'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentary_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(null=True, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mark',
            name='solution_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='classroom.solution'),
        ),
    ]
