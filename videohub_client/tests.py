#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplejson as json

from django.template.defaultfilters import slugify
from django.test import TestCase
import requests

from .models import VideohubVideo
from .serializers import VideohubVideoSerializer


class VideohubVideoTests(TestCase):

    def setUp(self):
        self.video = VideohubVideo.objects.create(
            id=1,
            title="Lake Dredge Appraisal Episode 2",
            description="Revolting Silt",
            keywords="Lake Dredge Appraisal Revoling Silt Episode 2"
        )

    def test_hub_url(self):
        with self.settings(VIDEOHUB_VIDEO_URL="http://onionstudios.com/video/x-{}"):
            hub_url = self.video.get_hub_url()
            self.assertEquals(
                hub_url,
                "http://onionstudios.com/video/x-{}".format(self.video.id))

    def test_embed_url(self):
        with self.settings(VIDEOHUB_EMBED_URL="http://onionstudios.com/embed?id={}"):
            embed_url = self.video.get_embed_url()
            self.assertEquals(
                embed_url,
                "http://onionstudios.com/embed?id={}".format(self.video.id))

    def test_api_url(self):
        with self.settings(VIDEOHUB_API_URL="http://onionstudios.com/api/videos/{}"):
            api_url = self.video.get_api_url()
            self.assertEquals(
                api_url,
                "http://onionstudios.com/api/videos/{}".format(self.video.id))

    def test_serializer_has_urls(self):
        with self.settings(VIDEOHUB_VIDEO_URL="http://onionstudios.com/video/x-{}"), \
                self.settings(VIDEOHUB_EMBED_URL="http://onionstudios.com/embed?id={}"), \
                self.settings(VIDEOHUB_API_URL="http://onionstudios.com/api/videos/{}"):
            hub_url = self.video.get_hub_url()
            embed_url = self.video.get_embed_url()
            api_url = self.video.get_api_url()
            serializer = VideohubVideoSerializer(self.video)
            self.assertEquals(hub_url, serializer.data["hub_url"])
            self.assertEquals(embed_url, serializer.data["embed_url"])
            self.assertEquals(api_url, serializer.data["api_url"])

    def test_search_hub(self):
        with self.settings(VIDEOHUB_API_SEARCH_URL=VideohubVideo.DEFAULT_VIDEOHUB_API_SEARCH_URL), \
                self.settings(VIDEOHUB_API_TOKEN="Token 5bd1421dc4b162426bfa551e2b9c3e8407758820"):

            url = VideohubVideo.DEFAULT_VIDEOHUB_API_SEARCH_URL

            try:
                res = requests.get(url)
            except:
                return
            if not res.status_code == 200:
                return

            res = VideohubVideo.search_videohub("wolf")
            self.assertIn("results", res)

    # def test_hub_url_with_unicode(self):
    #     """Make sure get_hub_url can handle unicode characters properly."""
    #
    #     video_1 = VideohubVideo.objects.create(title=u"\u2019The Facts Of Life\u2019")
    #     video_2 = VideohubVideo.objects.create(title=u"‘The Facts Of Life’")
    #     video_3 = VideohubVideo.objects.create(title="‘The Facts Of Life’")
    #
    #     video_1.save()
    #     video_2.save()
    #     video_3.save()
    #
    #     print video_1.get_hub_url()
    #
    #     self.assertEqual(video_1.get_hub_url(), VideohubVideoSerializer(video_1).data["hub_url"])
    #     self.assertEqual(video_2.get_hub_url(), VideohubVideoSerializer(video_2).data["hub_url"])
    #     self.assertEqual(video_3.get_hub_url(), VideohubVideoSerializer(video_3).data["hub_url"])
