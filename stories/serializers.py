from rest_framework import serializers

from stories.models import Paragraph, Story
from users.serializers import UserSerializer


class ParagraphSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Paragraph
        fields = ('author', 'content', 'created_at')


class BasicStorySerializer(serializers.ModelSerializer):
    master = UserSerializer()
    category = serializers.StringRelatedField()
    excerpt = serializers.SerializerMethodField()

    def get_excerpt(self, obj):
        return str(obj.paragraphs.first())

    class Meta:
        model = Story
        fields = ('title', 'master', 'feature_image', 'category')
