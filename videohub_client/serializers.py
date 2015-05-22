from djbetty.serializers import ImageFieldSerializer
from rest_framework import serializers

from .models import VideohubVideo


class VideohubVideoSerializer(serializers.ModelSerializer):
    image = ImageFieldSerializer(required=False)
    hub_url = serializers.CharField(source="get_hub_url", read_only=True)
    embed_url = serializers.CharField(source="get_embed_url", read_only=True)
    api_url = serializers.CharField(source="get_api_url", read_only=True)

    class Meta:
        model = VideohubVideo

    def to_internal_value(self, data):
        """Prevent DRF from creating a new row."""
        identity = data.get("id")
        obj = None

        if hasattr(self, "opts"):
            ModelClass = self.opts.model
        else:
            ModelClass = self.Meta.model

        if identity:
            try:
                obj = ModelClass.objects.get(id=identity)
            except ModelClass.DoesNotExist:
                pass
            else:
                dirty = False
                for field_name, field_serializer in self.fields.items():
                    val = field_serializer.to_internal_value(data.get(field_name))
                    if hasattr(obj, field_name):
                        if getattr(obj, field_name) != val:
                            setattr(obj, field_name, val)
                            dirty = True
                if dirty:
                    obj.save()
        if obj is None:
            obj = super(VideohubVideoSerializer, self).to_internal_value(data)
        return obj
