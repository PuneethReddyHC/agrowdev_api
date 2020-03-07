import markdown
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class MovieInfo (PostBaseInfo):
    """
    Movie Basic Information
    """
    directors = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "director", help_text = "director")
    actors = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "actor", help_text = "actor")
    region = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "region", help_text = "region")
    language = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "language", help_text = "language")
    length = models.IntegerField(default = 0, null = True, blank = True, verbose_name = "Duration", help_text = "Duration")

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.title

    def save (self, *args, **kwargs):
        # Set the type manually
        self.post_type = 'movie'
        super (MovieInfo, self) .save (*args, **kwargs)


class MovieDetail(models.Model):
    """
    Movie details
    """
    LANGUAGE = (
        ("CN", "Chinese"),
        ("EN", "English")
    )
    language = models.CharField(null = True, blank = True, max_length = 5, choices = LANGUAGE, verbose_name = "article details language category", help_text = "two language categories are now available")
    movie_info = models.ForeignKey(MovieInfo, null = True, blank = True, related_name = 'details', verbose_name = "content",
                                   help_text = "content", on_delete = models.CASCADE)
    origin_content = models.TextField(null = False, blank = False, verbose_name = "original content", help_text = "original content")
    formatted_content = models.TextField(verbose_name = "processed content", help_text = "processed content")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")
    update_time = models.DateTimeField(auto_now = True, null = True, blank = True, verbose_name = "modification time",
                                       help_text = "modification time")

    def save (self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown (self.origin_content, extensions = MARKDOWN_EXTENSIONS,
                                                   extension_configs = MARKDOWN_EXTENSION_CONFIGS, lazy_ol = False)
        super (MovieDetail, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.movie_info.title

    class Meta:
        verbose_name = "Movie Details"
        verbose_name_plural = verbose_name + 'list'