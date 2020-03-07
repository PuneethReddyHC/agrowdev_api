# Generated by Django 2.2.10 on 2020-03-07 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
        ('comment', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentinfo',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='user.GuestProfile', verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='parent_comment',
            field=models.ForeignKey(blank=True, help_text='root comment', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comment', to='comment.CommentInfo', verbose_name='root comment'),
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.PostBaseInfo', verbose_name='post'),
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='reply_to_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='be_comments', to='user.GuestProfile', verbose_name='Responded'),
        ),
        migrations.AddField(
            model_name='commentinfo',
            name='reply_to_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='comment.CommentInfo', verbose_name='Parent Comment'),
        ),
        migrations.AddField(
            model_name='commentdetail',
            name='comment_info',
            field=models.OneToOneField(blank=True, help_text='Basic Information', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='comment.CommentInfo', verbose_name='Basic Information'),
        ),
    ]
