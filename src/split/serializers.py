from rest_framework import serializers

from src.split.models import Split


class CreateSplitSerializer(serializers.ModelSerializer):
    config = serializers.JSONField(required=False)

    class Meta:
        model = Split
        fields = ('id', 'config', 'original_log')


class SplitSerializer(serializers.ModelSerializer):
    training_log = serializers.SerializerMethodField()

    def get_training_log(self, split):
        return split.train_log.pk if split.train_log is not None else None

    class Meta:
        model = Split
        fields = ('id', 'original_log', 'type', 'test_log', 'training_log')
