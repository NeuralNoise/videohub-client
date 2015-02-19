from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase

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
        with self.settings(VIDEOHUB_VIDEO_URL_TEMPLATE="http://onionstudios.com/video/{slug}-{hub_id}"):
            hub_url = self.video.get_hub_url()
            slug = slugify(self.video.title)
            self.assertEquals(hub_url, "http://onionstudios.com/video/{}-{}".format(slug, self.video.id))

    def test_embed_url(self):
        with self.settings(VIDEOHUB_EMBED_URL_TEMPLATE="http://onionstudios.com/embed?id={hub_id}"):
            embed_url = self.video.get_embed_url()
            self.assertEquals(embed_url, "http://onionstudios.com/embed?id={}".format(self.video.id))

    def test_hub_url_serializer(self):
        """Make sure we send along the hub_url in the serializer."""
        with self.settings(VIDEOHUB_VIDEO_URL_TEMPLATE="http://onionstudios.com/video/{slug}-{hub_id}"):
            hub_url = self.video.get_hub_url()
            serializer = VideohubVideoSerializer(self.video)
            self.assertEquals(hub_url, serializer.data["hub_url"])
