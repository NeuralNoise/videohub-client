from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from djbetty.fields import ImageField


class VideohubVideo(models.Model):
    """A reference to a video on the onion videohub."""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    keywords = models.TextField(blank=True, default="")
    image = ImageField(null=True, blank=True, alt_field="_image_alt", caption_field="_image_caption")
    _image_alt = models.CharField(null=True, blank=True, editable=False, max_length=255)
    _image_caption = models.CharField(null=True, blank=True, editable=False, max_length=255)

    def get_hub_url(self):
        slug = slugify(self.title)
        hub_url_template = getattr(
            settings, "VIDEOHUB_VIDEO_URL_TEMPLATE",
            "http://onionstudios.com/video/{slug}-{hub_id}")
        return hub_url_template.format(slug=slug, hub_id=self.id)
