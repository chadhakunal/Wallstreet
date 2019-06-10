# Generated by Django 2.1.2 on 2019-02-20 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buytabletype1',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='buytabletype2',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='buytabletype3',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='buytabletype4',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='buytabletype5',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='selltabletype1',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='selltabletype2',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='selltabletype3',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='selltabletype4',
            name='entryTime',
        ),
        migrations.RemoveField(
            model_name='selltabletype5',
            name='entryTime',
        ),
        migrations.AddField(
            model_name='company',
            name='endPointer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='startPointer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userhistory',
            name='pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.Company'),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='companyOwned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.Company'),
        ),
    ]
