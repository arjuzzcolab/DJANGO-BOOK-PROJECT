# Generated by Django 4.2.15 on 2024-09-03 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookapp', '0002_book_quantity'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='bookapp.book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.logintable')),
            ],
        ),
        migrations.CreateModel(
            name='cartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookapp.book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.cart')),
            ],
        ),
    ]
