import hashlib
from django.db import models
from material.models import MaterialSocial, MaterialMaster


class NavigationLink(models.Model):
    """
    Custom navigation
    """
    TARGET_TYPE = (
    ("_blank", "blank-Browser always loads the target document in a newly opened, unnamed window."),
    ("_self",
    "self-The value of this target is the default target for all <a> tags without a target specified, which causes the target document to be loaded and displayed in the same frame or window as the source document. This target is redundant and unnecessary unless Used with the target attribute in the document title <base> tag. "),
    ("_parent", "parent-This target causes the document to load into the parent window or frameset containing frames referenced by hyperlinks. If this reference is in a window or in a top-level frame, it is equivalent to target _self." ),
    ("_top", "top-this target causes the document to load into the window containing this hyperlink. Using the _top target will clear all included frames and load the document into the entire browser window.")
    )
    name = models.CharField(max_length = 30, verbose_name = "name", help_text = "name")
    en_name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "English name", help_text = "English name")
    desc = models.CharField(max_length = 100, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "English introduction", help_text = "English introduction")
    image = models.ImageField(upload_to = "base/friendlink/image/%y/%m", null = True, blank = True, verbose_name = "picture",
    help_text = "picture")
    url = models.CharField(max_length = 200, verbose_name = "link", help_text = "link")
    target = models.CharField(max_length = 10, choices = TARGET_TYPE, null = True, blank = True, verbose_name = "Target category",
    help_text = "corresponds to the target attribute in the a tag")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
    # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (NavigationLink, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Custom Navigation"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class SiteInfo(models.Model):
    name = models.CharField(default = "", max_length = 20, verbose_name = "name", help_text = "name")
    en_name = models.CharField(null = True, blank = True, max_length = 20, verbose_name = "Name English", help_text = "Name English")
    desc = models.CharField(default = "", max_length = 150, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(null = True, blank = True, max_length = 150, verbose_name = "Introduction", help_text = "Introduction")
    keywords = models.CharField(default = "", max_length = 300, verbose_name = "keyword", help_text = "keyword")
    icon = models.ImageField(upload_to = "base/site/image/%y/%m", null = True, blank = True, verbose_name = "icon",
                                help_text = "icon")
    background = models.ImageField(upload_to = "base/site/image/%y/%m", null = True, blank = True, verbose_name = "background image",
                                   help_text = "background image")
    api_base_url = models.URLField(max_length = 30, null = False, blank = False, verbose_name = 'API InterfaceBaseURL')
    navigations = models.ManyToManyField(NavigationLink, through = "SiteInfoNavigation", through_fields = (
        'site', 'navigation'), verbose_name = 'Custom Navigation', help_text = 'Custom Navigation')
    copyright = models.CharField(default = "", max_length = 100, verbose_name = "copyright", help_text = "copyright")
    copyright_desc = models.CharField(default = "", max_length = 300, verbose_name = "copyright Chinese", help_text = "copyright Chinese")
    copyright_desc_en = models.CharField(default = "", max_length = 300, verbose_name = "copyright English", help_text = "copyright English")
    icp = models.CharField(default = "", max_length = 20, verbose_name = "ICP", help_text = "ICP")
    is_live = models.BooleanField(default = False, verbose_name = "is active", help_text = "is active")
    is_force_refresh = models.BooleanField(default = False, verbose_name = "whether to force a refresh", help_text = "is used to control whether the front-end page is forced to refresh the local cache")
    force_refresh_time = models.DateTimeField(null = True, blank = True, verbose_name = "force refresh time",
                            help_text = "The time will be returned to the front end. The front end compares the local storage time of the browser with this time. If the forced refresh time of the browser's local storage is earlier than this time, a forced refresh of the browser's local cache will be performed" )
    access_password = models.CharField(max_length = 20, null = True, blank = True, verbose_name = "access password", help_text = "browse password")
    access_password_encrypt = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "Browse password encryption",
                help_text = "Access password encryption")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def __str__ (self):
        return self.name

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        if self.access_password:
            md5 = hashlib.md5 ()
            md5.update (self.access_password.encode ('utf8'))
            self.access_password_encrypt = md5.hexdigest ()
        else:
            self.access_password_encrypt = ''
        super (SiteInfo, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Site Information"
        verbose_name_plural = verbose_name + 'list'


class BloggerInfo(models.Model):
    name = models.CharField(default = "", max_length = 20, verbose_name = "name", help_text = "name")
    en_name = models.CharField(null = True, blank = True, max_length = 20, verbose_name = "Name English", help_text = "Name English")
    desc = models.CharField(default = "", max_length = 300, verbose_name = "Introduction", help_text = "Introduction")
    en_desc = models.CharField(default = "", max_length = 300, verbose_name = "Introduction", help_text = "Introduction")
    avatar = models.ImageField(upload_to = "base/avatar/image/%y/%m", null = True, blank = True, verbose_name = "avatar",
                               help_text = "100 *100")
    background = models.ImageField(upload_to = "base/background/image/%y/%m", null = True, blank = True, verbose_name = "background image",
                                   help_text = "333 *125")
    socials = models.ManyToManyField(MaterialSocial, through = 'BloggerSocial', through_fields = ('blogger', 'social'))
    masters = models.ManyToManyField(MaterialMaster, through = 'BloggerMaster', through_fields = ('blogger', 'master'))
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def save (self, *args, **kwargs):
        # Provide default values ​​for English title and description
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super (BloggerInfo, self) .save (*args, **kwargs)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class BloggerSocial(models.Model):
    name = models.CharField(default = "", max_length = 20, verbose_name = "name", help_text = "name")
    blogger = models.ForeignKey(BloggerInfo, verbose_name = "person", help_text = "person", on_delete = models.CASCADE)
    social = models.ForeignKey(MaterialSocial, verbose_name = "Social Platform", help_text = "Social Platform", on_delete = models.CASCADE)
    index = models.IntegerField(default = 0, verbose_name = "order", help_text = "order")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Social Information"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class BloggerMaster(models.Model):
    name = models.CharField(default = "", max_length = 20, verbose_name = "name", help_text = "name")
    blogger = models.ForeignKey(BloggerInfo, verbose_name = "person", help_text = "person", on_delete = models.CASCADE)
    master = models.ForeignKey(MaterialMaster, verbose_name = "skill", help_text = "skill", on_delete = models.CASCADE)
    index = models.IntegerField(default = 0, verbose_name = "order", help_text = "order")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Skill Information"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class SiteInfoNavigation(models.Model):
    name = models.CharField(default = "", max_length = 20, verbose_name = "name", help_text = "name")
    site = models.ForeignKey(SiteInfo, verbose_name = "website", help_text = "website", on_delete = models.CASCADE)
    navigation = models.ForeignKey(NavigationLink, verbose_name = "navigation", help_text = "navigation", on_delete = models.CASCADE)
    index = models.IntegerField(default = 0, verbose_name = "order", help_text = "order")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Navigation Information"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name


class FriendLink(models.Model):
    """
    Links
    """
    name = models.CharField(max_length = 30, verbose_name = "name", help_text = "name")
    desc = models.CharField(max_length = 100, verbose_name = "Introduction", help_text = "Introduction")
    image = models.ImageField(upload_to = "base/friendlink/image/%y/%m", null = True, blank = True, verbose_name = "picture",
                              help_text = "picture")
    url = models.URLField(max_length = 200, verbose_name = "link", help_text = "link")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    class Meta:
        verbose_name = "Friendly Link"
        verbose_name_plural = verbose_name + 'list'

    def __str__ (self):
        return self.name