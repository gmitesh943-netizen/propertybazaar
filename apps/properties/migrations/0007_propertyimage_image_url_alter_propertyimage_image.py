from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_property_age_of_property_property_brochure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyimage',
            name='image_url',
            field=models.URLField(blank=True, help_text='External image URL (used on Render/cloud)', max_length=500),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='property_images/'),
        ),
    ]
