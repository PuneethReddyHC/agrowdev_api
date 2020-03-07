from django.db import models

from datetime import datetime

from material.models import MaterialCategory, MaterialTag, MaterialPicture, PostBaseInfo


class AlbumInfo(PostBaseInfo):
    """
    Atlas basic information
    """
    pictures = models.ManyToManyField(MaterialPicture, through = "AlbumPhoto", through_fields = ('album', 'picture'),
                                      verbose_name = "picture", help_text = "picture")

    def save (self, *args, **kwargs):
        self.post_type = 'album'
        super (AlbumInfo, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.title

    class Meta:
        verbose_name = "Atlas"
        verbose_name_plural = verbose_name + 'list'


class AlbumPhoto(models.Model):
    """
    Atlas pictures
    """
    album = models.ForeignKey(AlbumInfo, null = False, blank = False, verbose_name = "atlas", help_text = "atlas", on_delete = models.CASCADE)
    picture = models.ForeignKey(MaterialPicture, null = False, blank = False, verbose_name = "picture", help_text = "picture", on_delete = models.CASCADE)
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Atlas Pictures"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.album.title