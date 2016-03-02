import re

import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from videohub_client.models import VideohubVideo


class Command(BaseCommand):

    help = "Store new channel ID foreign key from Videhub for all existing videos"

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            default=False,
            help='Read-only check (preview) mode')

    def handle(self, *args, **options):

        # If any video fails, continue trying the rest before we raise error
        failed = []
        for video in VideohubVideo.objects.filter(channel_id__isnull=True):

            url = video.get_api_url()
            headers = {
                'Authorization': 'Token ' + settings.VIDEOHUB_SECRET_TOKEN,
                'Content-Type': 'application/json'
            }
            # Ensure protocol specified. VH does not yet support SSL.
            if not re.match(r'https?:', url):
                url = 'http:' + url

            resp = requests.get(url, headers=headers)

            if resp.ok:
                channel = resp.json()['channel']
                print('[{}] {} --> [{}] {}'.format(video.id,
                                                   video.title.strip().encode('utf-8')[:50],
                                                   channel['id'],
                                                   channel['name'].encode('utf-8')
                                                   ))
                if not options['check']:
                    video.channel_id = channel['id']
                    video.save()
            else:
                self.stderr.write(self.style.ERROR('Video request failed: {} --> {} {}'.format(
                    url,
                    resp.status_code,
                    resp.reason)))
                failed.append(video)

        if failed:
            raise CommandError('Failed to update {} video(s): {}'.format(
                len(failed),
                [f.id for f in failed]))
