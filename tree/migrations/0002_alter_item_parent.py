# Generated by Django 4.2.4 on 2024-02-23 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tree.item'),
        ),
    ]