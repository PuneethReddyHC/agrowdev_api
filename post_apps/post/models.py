from django.db import models
import markdown

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class PostInfo(PostBaseInfo):
    """
    Post basic information
    """

    def save (self, *args, **kwargs):
        self.post_type = 'post'
        super (PostInfo, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = verbose_name + 'list'


class PostDetail(models.Model):
    """
    Post details
    """
    LANGUAGE = (
        ("CN", "Chinese"),
        ("EN", "English")
    )
    language = models.CharField(null = True, blank = True, max_length = 5, choices = LANGUAGE, verbose_name = "post details language category", help_text = "two language categories are now available")
    post_info = models.ForeignKey(PostInfo, null = True, blank = True, related_name = 'details', verbose_name = "content", help_text = "content", on_delete = models.CASCADE)
    origin_content = models.TextField(null = False, blank = True, verbose_name = "original content", help_text = "original content")
    formatted_content = models.TextField(verbose_name = "processed content", help_text = "processed content")
    add_time = models.DateTimeField(null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")
    update_time = models.DateTimeField(null = True, blank = True, verbose_name = "modification time",
                                       help_text = "modification time")

    def save (self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown (self.origin_content, extensions = MARKDOWN_EXTENSIONS,
                                                   extension_configs = MARKDOWN_EXTENSION_CONFIGS, lazy_ol = False)
        super (PostDetail, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.post_info.title

    class Meta:
        verbose_name = "Post Details"
        verbose_name_plural = verbose_name + 'list'