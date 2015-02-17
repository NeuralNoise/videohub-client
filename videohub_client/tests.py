from django.core.urlresolvers import reverse
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
        with self.settings(VIDEOHUB_VIDEO_URL_TEMPLATE="http://onionstudios.com/video/{hub_id}/"):
            hub_url = self.video.get_hub_url()
            self.assertEquals(hub_url, "http://onionstudios.com/video/1/")

    def test_hub_url_serializer(self):
        """Make sure we send along the hub_url in the serializer."""
        with self.settings(VIDEOHUB_VIDEO_URL_TEMPLATE="http://onionstudios.com/video/{hub_id}/"):
            hub_url = self.video.get_hub_url()
            serializer = VideohubVideoSerializer(self.video)
            self.assertEquals(hub_url, serializer.data["hub_url"])
