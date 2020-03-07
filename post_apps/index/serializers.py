# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from drf_haystack.serializers import HighlighterMixin, HaystackSerializer

from post.search_indexes import PostDetailIndex
from comment.search_indexes import CommentDetailIndex
from post_apps.utils.CustomHighlighter import CustomHighlighter


class SearchSerializer(HighlighterMixin, HaystackSerializer):
    """
    搜索Serializer
    """
    highlighter_css_class = "search-highlight"
    highlighter_html_tag = "em"
    highlighter_class = CustomHighlighter

    class Meta:
        index_classes = (PostDetailIndex, CommentDetailIndex)
        fields = ('title', 'author', 'add_time', 'update_time', 'link', 'type')