from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_bankoffer_last_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='builders/logos/')),
                ('description', models.TextField(blank=True)),
                ('stat1_value', models.CharField(help_text='e.g. 124.3 Mn sqft', max_length=50)),
                ('stat1_label', models.CharField(help_text='e.g. Delivered projects till date', max_length=100)),
                ('stat2_value', models.CharField(help_text='e.g. 150,000+', max_length=50)),
                ('stat2_label', models.CharField(help_text='e.g. Happy families', max_length=100)),
                ('leader_name', models.CharField(max_length=255)),
                ('leader_designation', models.CharField(help_text='e.g. CEO, Omaxe Limited', max_length=255)),
                ('leader_image', models.ImageField(upload_to='builders/leaders/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='builder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties', to='properties.builder'),
        ),
    ]
