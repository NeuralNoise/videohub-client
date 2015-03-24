try:
    import json
except ImportError:
    import simplejson as json

from django.template.defaultfilters import slugify
from django.test import TestCase
from django.test.client import Client
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
        with self.settings(VIDEOHUB_VIDEO_URL="http://onionstudios.com/video/{}"):
            hub_url = self.video.get_hub_url()
            slug = slugify(self.video.title)
            self.assertEquals(hub_url, "http://onionstudios.com/video/{}-{}".format(slug, self.video.id))

    def test_embed_url(self):
        with self.settings(VIDEOHUB_EMBED_URL="http://onionstudios.com/embed?id={}"):
            embed_url = self.video.get_embed_url()
            self.assertEquals(embed_url, "http://onionstudios.com/embed?id={}".format(self.video.id))

    def test_api_url(self):
        with self.settings(VIDEOHUB_API_URL="http://onionstudios.com/api/v0/videos/{}"):
            api_url = self.video.get_api_url()
            self.assertEquals(api_url, "http://onionstudios.com/api/v0/videos/{}".format(self.video.id))

    def test_serializer_has_urls(self):
        with self.settings(VIDEOHUB_VIDEO_URL="http://onionstudios.com/video/{}"), \
             self.settings(VIDEOHUB_EMBED_URL="http://onionstudios.com/embed?id={}"), \
             self.settings(VIDEOHUB_API_URL="http://onionstudios.com/api/v0/videos/{}"):
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

            client = Client()
            payload = {"query": "wolf"}
            res = client.post(url, data=json.dumps(payload), content_type="application/json")
            self.assertEqual(res.status_code, 200)
            content = res.data
            self.assertIn("facets", content)
            self.assertIn("counts", content)
            self.assertIn("results", content)
