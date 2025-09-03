from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('owner','Owner'), ('sitter','Sitter'), ('both','Both')], default='owner', max_length=10),
        ),
    ]
