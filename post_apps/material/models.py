import hashlib

from django.db import models

from user.models import GuestProfile
from settings import SITE_BASE_URL

class MaterialCategory(models.Model):
    """
    Material category
    """
    CATEGORY_LEVEL = (
        ("1", "First Class"),
        ("2", "secondary category"),
        ("3", "tertiary category")
    )
    CATEGORY_TYPE = (
        ("posts", "Posts category"),
        ("posts/category", "Posts category"),
        ("albums", "Atlas total classification"),
        ("albums/category", "Atlas classification"),
        ("movies", "Movie Category"),
        ("movies/category", "Movie Category"),
        ("readings", "Reading Category"),
        ("readings/category", "readings"),
        ("books", "General Books"),
        ("books/category", "Books/category"),
        ("book/notes", "Total Reading Notes Category"),
        ("book/notes/category", "Reading Notes Category"),
    )
    name = models.CharField(max_length = 30, default = "", verbose_name = "category name", help_text = "category name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "English name", help_text = "English name")
    category_type = models.CharField(max_length = 30, choices = CATEGORY_TYPE, verbose_name = "route encoding", help_text = "for configuring route redirection")
    desc = models.TextField(null = True, blank = True, verbose_name = "category description", help_text = "category description")
    en_desc = models.TextField(null = True, blank = True, verbose_name = "category description", help_text = "category description")
    image = models.ImageField(upload_to = "comment/category/image/%Y/%m", null = True, blank = True, help_text = "picture")
    category_level = models.CharField(max_length = 20, choices = CATEGORY_LEVEL, verbose_name = "Category level", help_text = "Category level")
    parent_category = models.ForeignKey("self", null = True, blank = True, verbose_name = "parent category level", help_text = "parent category",
                                        related_name = "sub_category", on_delete = models.CASCADE)
    is_active = models.BooleanField(default = True, verbose_name = "is active", help_text = "is active")
    is_tab = models.BooleanField(default = True, verbose_name = "whether to navigate", help_text = "whether to navigate")
    index = models.IntegerField(default = 0, verbose_name = "sort", help_text = "sort")
    add_time = models.DateTimeField(auto_now_add = True, verbose_name = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (MaterialCategory, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return '{0}-{1}-{2}'. format (self.name, self.get_category_type_display (), self.get_category_level_display ())


class MaterialTag(models.Model):
    """
    Material tag
    """
    name = models.CharField(max_length = 30, null = False, blank = False, verbose_name = "tag name", help_text = "tag name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "English name", help_text = "English name")
    category = models.ForeignKey(MaterialCategory, null = True, blank = True, verbose_name = "category", help_text = "category", on_delete = models.CASCADE)
    color = models.CharField(max_length = 20, default = "blue", verbose_name = "color", help_text = "color")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        super (MaterialTag, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class MaterialLicense(models.Model):
    """
    Material License
    """
    COLOR_TYPE = (
        ("# 878D99", "gray"),
        ("# 409EFF", "blue"),
        ("# 67C23A", "green"),
        ("# EB9E05", "Yellow"),
        ("# FA5555", "Red")
    )
    name = models.CharField(max_length = 30, null = False, blank = False, verbose_name = "copyright name", help_text = "copyright name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "English name", help_text = "English name")
    desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    link = models.URLField(null = True, blank = True, verbose_name = "copyright reference link", help_text = "copyright reference link")
    color = models.CharField(max_length = 20, default = "blue", choices = COLOR_TYPE, verbose_name = "color", help_text = "color")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (MaterialLicense, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Authorization"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class MaterialCamera(models.Model):
    """
    Camera model
    """
    device = models.CharField(max_length = 30, verbose_name = "device", help_text = "device")
    version = models.CharField(max_length = 200, verbose_name = "version", help_text = "version")
    environment = models.CharField(max_length = 200, verbose_name = "environment", help_text = "environment")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Camera Model"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.device


class MaterialPicture(models.Model):
    """
    Material picture
    """
    title = models.CharField(max_length = 100, null = False, blank = False, verbose_name = "title", help_text = "title")
    en_title = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "subtitle", help_text = "subtitle")
    desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Summary", help_text = "Summary")
    image = models.ImageField(upload_to = "comment/picture/image/%Y/%m", null = True, blank = True, verbose_name = "picture",
                              help_text = "picture")
    camera = models.ForeignKey(MaterialCamera, null = True, blank = True, verbose_name = "shooting camera", help_text = "shooting camera", on_delete = models.CASCADE)
    link = models.URLField(null = True, blank = True, verbose_name = "link", help_text = "link")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_title:
            self.en_title = self.title
        if not self.en_desc:
            self.en_desc = self.desc
        super (MaterialPicture, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Picture"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.title


class PostBaseInfo(models.Model):
    """
    Post Basic Information
    """
    POST_TYPE = (
        ("post", "post"),
        ("album", "Atlas"),
        ("movie", "movie"),
        ("book", "Book"),
        ("book/note", "book note")
    )
    FRONT_IMAGE_TYPE = (
        ("0", "None"),
        ("1", "Small Picture"),
        ("2", "big picture")
    )
    title = models.CharField(max_length = 100, null = False, blank = False, verbose_name = "title", help_text = "title")
    en_title = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "English title", help_text = "English title")
    desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 255, null = True, blank = True, verbose_name = "English introduction", help_text = "English introduction")
    author = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "author", help_text = "author")
    category = models.ForeignKey(MaterialCategory, null = False, blank = False, verbose_name = "category", help_text = "category", on_delete = models.CASCADE)
    tags = models.ManyToManyField(MaterialTag, through = "PostTag", through_fields = ('post', 'tag'))
    post_type = models.CharField(max_length = 20, choices = POST_TYPE, null = True, blank = True, verbose_name = "POST category",
                                 help_text = "POST category")
    click_num = models.IntegerField(default = 0, verbose_name = "clicks", help_text = "clicks")
    like_num = models.IntegerField(default = 0, verbose_name = "Number of Likes", help_text = "Number of Likes")
    comment_num = models.IntegerField(default = 0, verbose_name = "Number of Comments", help_text = "Number of Comments")
    front_image = models.ImageField(upload_to = "post/image/%y/%m", null = True, blank = True, verbose_name = "cover image",
                                    help_text = "big picture 833 *217, small picture 243 *207")
    front_image_type = models.CharField(max_length = 20, default = "0", choices = FRONT_IMAGE_TYPE, verbose_name = "cover image category",
                                        help_text = "cover art category")
    license = models.ForeignKey(MaterialLicense, null = True, blank = True, verbose_name = "copyright", help_text = "copyright", on_delete = models.CASCADE)
    is_hot = models.BooleanField(default = False, verbose_name = "is it hot", help_text = "is it hot")
    is_recommend = models.BooleanField(default = False, verbose_name = "Recommended", help_text = "Recommended")
    is_banner = models.BooleanField(default = False, verbose_name = "is it Banner", help_text = "is it Banner")
    is_active = models.BooleanField(default = True, verbose_name = "is active", help_text = "is active")
    is_commentable = models.BooleanField(default = True, verbose_name = "Can comment", help_text = "Can comment")
    browse_password = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "browse password", help_text = "browse password")
    browse_password_encrypt = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Browse password encryption",
                                               help_text = "Browse password encryption")
    index = models.IntegerField(default = 0, verbose_name = "Sticked", help_text = "Sticked")
    add_time = models.DateTimeField(null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_title:
            self.en_title = self.title
        if not self.en_desc:
            self.en_desc = self.desc
        if self.browse_password and len (self.browse_password)> 0:
            md5 = hashlib.md5 ()
            md5.update (self.browse_password.encode ('utf8'))
            self.browse_password_encrypt = md5.hexdigest ()
        else:
            self.browse_password_encrypt = None
        super (PostBaseInfo, self) .save (*args, **kwargs)

    # This method is mainly used to return post access links in RSS
    def get_absolute_url (self):
        return '{0}/{1}/{2}'. format (SITE_BASE_URL, self.post_type, self.id)

    class Meta:
        verbose_name = "All blog posts"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.title


class PostTag(models.Model):
    """
    Post tags
    """
    post = models.ForeignKey(PostBaseInfo, null = False, blank = False, verbose_name = "post", help_text = "post", on_delete = models.CASCADE)
    tag = models.ForeignKey(MaterialTag, null = False, blank = False, verbose_name = "tag", help_text = "tag", on_delete = models.CASCADE)
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.tag.name


class MaterialBanner(models.Model):
    """
    Carousel
    """
    title = models.CharField(max_length = 100, verbose_name = "title", help_text = "title")
    en_title = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "title", help_text = "title")
    image = models.ImageField(upload_to = "comment/banner/image/%y/%m", null = True, blank = True, verbose_name = "picture",
                              help_text = "picture")
    url = models.URLField(max_length = 200, verbose_name = "link", help_text = "link")
    category = models.ForeignKey(MaterialCategory, default = '1', null = False, blank = False, verbose_name = "category",
                                 help_text = "category", on_delete = models.CASCADE)
    index = models.IntegerField(default = 0, verbose_name = "order", help_text = "order")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_title:
            self.en_title = self.title
        super (MaterialBanner, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.title


class MaterialSocial(models.Model):
    """
    social platform
    """
    name = models.CharField(max_length = 30, verbose_name = "name", help_text = "name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "name", help_text = "name")
    desc = models.CharField(max_length = 100, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    image = models.ImageField(upload_to = "commentsocial/image/%y/%m", null = True, blank = True, verbose_name = "picture",
                              help_text = "picture")
    url = models.URLField(max_length = 200, verbose_name = "link", help_text = "link")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (MaterialSocial, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Social Platform"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class MaterialMaster(models.Model):
    """¡
    skill
    """
    name = models.CharField(max_length = 30, verbose_name = "name", help_text = "name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "name", help_text = "name")
    desc = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Introduction", help_text = "Introduction")
    image = models.ImageField(upload_to = "comment/master/image/%y/%m", null = True, blank = True, verbose_name = "picture",
                              help_text = "picture")
    url = models.URLField(max_length = 200, verbose_name = "link", help_text = "link")
    experience = models.FloatField(default = 0, verbose_name = "Proficiency", help_text = "Proficiency")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (MaterialMaster, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name