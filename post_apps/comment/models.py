import markdown
from django.db import models
import bleach, html
from base.utils import ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES, ALLOWED_PROTOCOLS

from material.models import PostBaseInfo
from user.models import GuestProfile
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS

class CommentInfo(models.Model):
    """
    Review basic information
    """
    post = models.ForeignKey(PostBaseInfo, null = False, blank = False, verbose_name = 'post', on_delete = models.CASCADE)
    author = models.ForeignKey(GuestProfile, null = True, blank = True, related_name = "comments", verbose_name = 'Author', on_delete = models.CASCADE)
    reply_to_author = models.ForeignKey(GuestProfile, null = True, blank = True, related_name = "be_comments",
                                        verbose_name = 'Responded', on_delete = models.CASCADE)
    comment_level = models.IntegerField(default = 0, verbose_name = "comment level", help_text = "comment level")
    parent_comment = models.ForeignKey("self", null = True, blank = True, related_name = "sub_comment", verbose_name = "root comment",
                                       help_text = "root comment", on_delete = models.CASCADE)
    reply_to_comment = models.ForeignKey("self", null = True, blank = True, related_name = 'reply_comment',
                                         verbose_name = 'Parent Comment', on_delete = models.CASCADE)
    like_num = models.IntegerField(default = 0, verbose_name = "Number of Likes", help_text = "Number of Likes")
    unlike_num = models.IntegerField(default = 0, verbose_name = "counter number", help_text = "counter number")
    comment_num = models.IntegerField(default = 0, verbose_name = "Number of Comments", help_text = "Number of Comments")
    is_hot = models.BooleanField(default = False, verbose_name = "is it hot", help_text = "is it hot")
    is_recommend = models.BooleanField(default = False, verbose_name = "Recommended", help_text = "Recommended")
    is_active = models.BooleanField(default = True, verbose_name = "is active", help_text = "is active")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Comment basic information"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return html.unescape (self.detail.formatted_content [: 100])


class CommentDetail(models.Model):
    """
    Comment details
    """
    comment_info = models.OneToOneField(CommentInfo, null = True, blank = True, related_name = 'detail',
                                        verbose_name = "Basic Information",
                                        help_text = "Basic Information", on_delete = models.CASCADE)
    origin_content = models.TextField(null = False, blank = False, verbose_name = "original content", help_text = "original content")
    formatted_content = models.TextField(null = True, blank = True, verbose_name = "processed content", help_text = "processed content")
    update_time = models.DateTimeField(auto_now = True, null = True, blank = True, verbose_name = "modification time",
                                       help_text = "modification time")

    def save (self, *args, **kwargs):
        self.formatted_content = bleach.clean (
            markdown.markdown (self.origin_content, extensions = MARKDOWN_EXTENSIONS, extension_configs = MARKDOWN_EXTENSION_CONFIGS, lazy_ol = False), ALLOWED_TAGS,
            ALLOWED_ATTRIBUTES, ALLOWED_STYLES,
            ALLOWED_PROTOCOLS, False, False)
        super (CommentDetail, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.comment_info.post.title

    class Meta:
        verbose_name = "Comment details"
        verbose_name_plural = verbose_name + 'list'