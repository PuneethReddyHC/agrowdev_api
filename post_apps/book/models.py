import markdown
import requests
import json
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from settings import DOUBAN_API_URL
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class BookInfo(PostBaseInfo):
    """
    Book basic information
    """
    DOUBAN_TYPE = (
        ("book", "Book"),
        ("movie", "movie")
    )
    book_image = models.ImageField(upload_to = "book/image/%y/%m", null = True, blank = True, verbose_name = "cover image",
                                   help_text = "big picture 833 *217, small picture 243 *207")
    is_reading = models.BooleanField(default = False, verbose_name = 'Whether reading', help_text = 'Whether reading')
    read_precentage = models.FloatField(default = 0.0, null = True, blank = True, verbose_name = 'Reading progress', help_text = 'Reading progress')
    douban_type = models.CharField(max_length = 255, choices = DOUBAN_TYPE, null = True, blank = True, verbose_name = "Douban resource type",
                                   help_text = "Douban Resource Type")
    douban_id = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "douban resource ID", help_text = "douban resource ID")
    douban_infos = models.TextField(null = True, blank = True, verbose_name = 'Douban Information', help_text = 'Douban Information')
    book_isbn10 = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "isbn10", help_text = "isbn10")
    book_isbn13 = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "isbn13", help_text = "isbn13")
    book_name = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Book Name", help_text = "Book Name")
    book_origin_name = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "book original name", help_text = "book original name")
    book_author = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Book Author", help_text = "Book Author")
    book_tags = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "book tags", help_text = "book tags")
    book_rating = models.CharField(max_length = 10, null = True, blank = True, verbose_name = "Book Douban Rating", help_text = "Book Douban Rating")
    book_publisher = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "publisher", help_text = "publisher")
    publish_date = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "Publish Date", help_text = "Publish Date")
    book_pages = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "total pages", help_text = "total pages")
    book_url = models.URLField(null = True, blank = True, verbose_name = "Book Douban Link", help_text = "Book Douban Link")
    book_api = models.URLField(null = True, blank = True, verbose_name = "Book API Link", help_text = "Book API Link")
    is_update_douban_info = models.BooleanField(default = False, verbose_name = 'Whether to update', help_text = 'It will automatically update all unfilled Douban information')

    def __str__ (self):
        return self.book_name

    def save (self, *args, **kwargs):
        self.post_type = 'book'
        # Douban Information
        if self.is_update_douban_info:
            douban_infos = requests.get (
                '{0}/{1}/{2}'. Format (DOUBAN_API_URL, self.douban_type, self.douban_id))
            douban_infos_dict = json.loads (douban_infos.text)
            if douban_infos_dict:
                if not self.book_isbn10:
                    self.book_isbn10 = douban_infos_dict ['isbn10']
                if not self.book_isbn13:
                    self.book_isbn13 = douban_infos_dict ['isbn13']
                if not self.book_name:
                    self.book_name = douban_infos_dict ['title']
                if not self.book_origin_name:
                    self.book_origin_name = douban_infos_dict ['origin_title']
                if not self.book_author:
                    self.book_author = ','. join (douban_infos_dict ['author'])
                if not self.book_tags:
                    self.book_tags = ','. join (item ['name'] for item in douban_infos_dict ['tags'])
                if not self.book_rating:
                    self.book_rating = douban_infos_dict ['rating'] ['average']
                if not self.book_publisher:
                    self.book_publisher = douban_infos_dict ['publisher']
                if not self.publish_date:
                    self.publish_date = douban_infos_dict ['pubdate']
                if not self.book_pages:
                    self.book_pages = douban_infos_dict ['pages']
                if not self.book_url:
                    self.book_url = douban_infos_dict ['alt']
                if not self.book_api:
                    self.book_api = douban_infos_dict ['url']
                self.douban_infos = douban_infos.text
            self.is_update_douban_info = False
        super (BookInfo, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = verbose_name + 'list'

class BookDetail (models.Model):
    """
    Book details
    """
    LANGUAGE = (
        ("CN", "Chinese"),
        ("EN", "English")
    )
    language = models.CharField (null = True, blank = True, max_length = 5, choices = LANGUAGE, verbose_name = "post details language category", help_text = "two language categories are now available")
    book_info = models.ForeignKey (BookInfo, null = True, blank = True, related_name = 'details', verbose_name = "content",
                                  help_text = "content", on_delete = models.CASCADE)
    origin_content = models.TextField (null = False, blank = False, verbose_name = "original content", help_text = "original content")
    formatted_content = models.TextField (verbose_name = "processed content", help_text = "processed content")
    add_time = models.DateTimeField (null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")
    update_time = models.DateTimeField (null = True, blank = True, verbose_name = "modification time",
                                       help_text = "modification time")

    def save (self, * args, ** kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown (self.origin_content, extensions = MARKDOWN_EXTENSIONS,
                                                   extension_configs = MARKDOWN_EXTENSION_CONFIGS, lazy_ol = False)

        super (BookDetail, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.book_info.title

    class Meta:
        verbose_name = "Book Details"
        verbose_name_plural = verbose_name + 'list'


class BookNoteInfo (PostBaseInfo):
    """
    Book Notes Basic Information
    """
    NOTE_TYPE = (
        ("1", "level 1"),
        ("2", "Secondary"),
        ("3", "third level")
    )
    book = models.ForeignKey (BookInfo, null = True, blank = True, verbose_name = 'Book', help_text = "Book", on_delete = models.CASCADE)
    chapter = models.CharField (max_length = 20, null = False, blank = False, default = "", verbose_name = "chapter", help_text = "own chapter")
    note_type = models.CharField (max_length = 20, null = True, blank = True, choices = NOTE_TYPE, verbose_name = "note level",
                                 help_text = "note level")
    parent_note = models.ForeignKey ("self", null = True, blank = True, verbose_name = "parent note", help_text = "parent note",
                                    related_name = "sub_note", on_delete = models.CASCADE)
    is_reading = models.BooleanField (default = False, verbose_name = "Whether reading", help_text = "Whether reading")
    is_completed = models.BooleanField (default = False, verbose_name = "Are you finished reading", help_text = "Are you finished reading")
    is_noted = models.BooleanField (default = False, verbose_name = "note completed?", help_text = "note completed?")

    def __str__ (self):
        return self.title

    def save (self, *args, **kwargs):
        # Set the type manually
        self.post_type = 'book / note'
        super (BookNoteInfo, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Book Notes"
        verbose_name_plural = verbose_name + 'list'

class BookNoteDetail(models.Model):
    """
    Book notes details
    """
    LANGUAGE = (
        ("CN", "Chinese"),
        ("EN", "English")
    )
    language = models.CharField(null = True, blank = True, max_length = 5, choices = LANGUAGE, verbose_name = "post details language category", help_text = "two language categories are now available")
    book_note_info = models.ForeignKey(BookNoteInfo, null = True, blank = True, related_name = 'details', verbose_name = "content",
                                       help_text = "content", on_delete = models.CASCADE)
    origin_content = models.TextField(null = False, blank = False, verbose_name = "original content", help_text = "original content")
    formatted_content = models.TextField(verbose_name = "processed content", help_text = "processed content")
    add_time = models.DateTimeField(null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")
    update_time = models.DateTimeField(null = True, blank = True, verbose_name = "modification time",
                                       help_text = "modification time")

    def save (self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown (self.origin_content, extensions = MARKDOWN_EXTENSIONS,
                                                   extension_configs = MARKDOWN_EXTENSION_CONFIGS, lazy_ol = False)
        super (BookNoteDetail, self) .save (*args, **kwargs)

    def __str__ (self):
        return self.book_note_info.title

    class Meta:
        verbose_name = "Book Note Details"
        verbose_name_plural = verbose_name + 'list'


class BookResource(models.Model):
    book = models.ForeignKey(BookInfo, verbose_name = u"Book", on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, verbose_name = u"name")
    download = models.FileField(max_length = 100, upload_to = "book/resource/%Y/%m", verbose_name = u"resource file")
    add_time = models.DateTimeField(auto_now_add = True, verbose_name = u"Add time")

    class Meta:
        verbose_name = u"Book Resources"
        verbose_name_plural = verbose_name

    def __unicode__ (self):
        return self.name