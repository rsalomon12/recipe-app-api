from rest_framework import serializers

from core.models import Tag, Ingridient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngridientSerializer(serializers.ModelSerializer):
    """serializer for ingridient objects"""

    class Meta:
        model = Ingridient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingridients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingridient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingridients', 'tags', 'time_minutes',
            'price', 'link'
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingridients = IngridientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
