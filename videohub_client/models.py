try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings
from django.db import models

from djbetty.fields import ImageField

import requests


class VideohubVideo(models.Model):
    """A reference to a video on the onion videohub."""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    keywords = models.TextField(blank=True, default="")
    image = ImageField(null=True, blank=True, alt_field="_image_alt", caption_field="_image_caption")
    _image_alt = models.CharField(null=True, blank=True, editable=False, max_length=255)
    _image_caption = models.CharField(null=True, blank=True, editable=False, max_length=255)

    # default values
    DEFAULT_VIDEOHUB_VIDEO_URL = "http://videohub.local/videos/x-{}"
    DEFAULT_VIDEOHUB_EMBED_URL = "http://videohub.local/embed?id={}"
    DEFAULT_VIDEOHUB_API_URL = "http://videohub.local/api/videos/{}/"
    DEFAULT_VIDEOHUB_API_SEARCH_URL = "http://videohub.local/api/videos/?search={}"

    @classmethod
    def get_serializer_class(cls):
        from .serializers import VideohubVideoSerializer
        return VideohubVideoSerializer

    @classmethod
    def search_videohub(cls, query, filters=None, status=None, sort=None, size=None, page=None):
        """searches the videohub given a query and applies given filters and other bits

        :see: https://github.com/theonion/videohub/blob/master/docs/search/post.md
        :see: https://github.com/theonion/videohub/blob/master/docs/search/get.md

        :param query: query terms to search by
        :type query: str
        :example query: "brooklyn hipsters"  # although, this is a little redundant...

        :param filters: video field value restrictions
        :type filters: dict
        :default filters: None
        :example filters: {"channel": "onion"} or {"series": "Today NOW"}

        :param status: limit the results to videos that are published, scheduled, draft
        :type status: str
        :default status: None
        :example status: "published" or "draft" or "scheduled"

        :param sort: video field related sorting
        :type sort: dict
        :default sort: None
        :example sort: {"title": "desc"} or {"description": "asc"}

        :param size: the page size (number of results)
        :type size: int
        :default size: None
        :example size": {"size": 20}

        :param page: the page number of the results
        :type page: int
        :default page: None
        :example page: {"page": 2}  # note, you should use `size` in conjunction with `page`

        :return: a dictionary of results and meta information
        :rtype: dict
        """
        # construct url
        url = getattr(settings, "VIDEOHUB_API_SEARCH_URL", cls.DEFAULT_VIDEOHUB_API_SEARCH_URL)

        # construct auth headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": settings.VIDEOHUB_API_TOKEN,
        }

        # add query
        url = url.format(query)

        # check for additional params
        if filters or status or sort or size or page:
            additional_params = ""
        else:
            additional_params = None

        if filters:
            for key, value in filters.items():
                additional_params += "&{}={}".format(key, value)

        if status:
            additional_params += "&status={}".format(status)

        if sort:
            for key, value in sort.items():
                if value == "desc":
                    additional_params += "&ordering=-{}".format(key)
                else:
                    additional_params += "&ordering={}".format(key)

        if size:
            additional_params += "&page_size={}".format(size)

        if page:
            additional_params += "&page={}".format(page)

        # add additional params if necessary
        if additional_params:
            url += additional_params

        # send request
        res = requests.get(url, headers=headers)

        # raise if not 200
        if res.status_code != 200:
            res.raise_for_status()

        # parse and return response
        return json.loads(res.content)

    def get_hub_url(self):
        """gets a canonical path to the detail page of the video on the hub

        :return: the path to the consumer ui detail page of the video
        :rtype: str
        """
        url = getattr(settings, "VIDEOHUB_VIDEO_URL", self.DEFAULT_VIDEOHUB_VIDEO_URL)
        return url.format(self.pk)

    def get_embed_url(self):
        """gets a canonical path to an embedded iframe of the video from the hub

        :return: the path to create an embedded iframe of the video
        :rtype: str
        """
        url = getattr(settings, "VIDEOHUB_EMBED_URL", self.DEFAULT_VIDEOHUB_EMBED_URL)
        return url.format(self.pk)

    def get_api_url(self):
        """gets a canonical path to the api detail url of the video on the hub

        :return: the path to the api detail of the video
        :rtype: str
        """
        url = getattr(settings, "VIDEOHUB_API_URL", self.DEFAULT_VIDEOHUB_API_URL)
        return url.format(self.pk)
