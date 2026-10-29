from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('institutions', '0010_groupmenupermission'),
    ]

    operations = [
        # Remove all existing rows (there are none yet, but safety first)
        migrations.RunSQL("DELETE FROM institutions_groupmenupermission;", migrations.RunSQL.noop),

        # Drop the unique constraint on group (OneToOneField → ForeignKey)
        migrations.AlterField(
            model_name='groupmenupermission',
            name='group',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='school_menu_permissions',
                to='auth.group',
            ),
        ),

        # Add school FK (nullable first so the column can be created, then enforce)
        migrations.AddField(
            model_name='groupmenupermission',
            name='school',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='group_menu_permissions',
                to='institutions.school',
            ),
        ),

        # Make school non-nullable
        migrations.AlterField(
            model_name='groupmenupermission',
            name='school',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='group_menu_permissions',
                to='institutions.school',
            ),
        ),

        # Add unique_together constraint
        migrations.AlterUniqueTogether(
            name='groupmenupermission',
            unique_together={('group', 'school')},
        ),
    ]
