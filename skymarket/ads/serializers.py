from rest_framework import serializers
from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_email = serializers.ReadOnlyField(source="author.email")
    ad_id = serializers.ReadOnlyField(source="ad.id")

    class Meta:
        model = Comment
        fields = ["pk", "text", "created_at", "ad_id", "author_email", "author_first_name", "author_last_name"]


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_email = serializers.ReadOnlyField(source="author.email")
    author_phone = serializers.ReadOnlyField(source="author.phone")

    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "description", "author_first_name", "author_last_name", "author_email", "author_phone"]
