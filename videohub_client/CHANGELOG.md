# videohub-client Change Log

## Version 0.2.0

### Support for ES filtering of Videohub channel

- Added DJES dependency
- `VideohubVideo` now inherits from DJES `Indexable` for easier ES mapping of nested videos
- Add `VidehubVideo.channel_id` foreign key and `migrate_channel_id` management command
