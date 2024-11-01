from rest_framework.serializers import ModelSerializer, SerializerMethodField
from freelance.models import Freelancer, Client

class FreelancerSerializer(ModelSerializer):
    user_bio = SerializerMethodField()
    user_username = SerializerMethodField()
    user_full_name = SerializerMethodField()
    type_user = SerializerMethodField()
    tags = SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = [
            'user',
            'user_username',
            'user_full_name',
            'user_bio',
            'type_user',
            'rating',
            'is_active',
            'created_at',
            'updated_at',
            'tags'
        ]
    
    def get_user_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else None

    def get_user_username(self, obj):
        return obj.user.username if obj.user else None
    
    def get_user_bio(self, obj):
        return obj.user.bio if obj.user else None

    def get_type_user(self, obj):
        return obj.user.profile.get_user_type_display() if obj.user and hasattr(obj.user, 'profile') else None

    def get_tags(self, obj):
        # Retorna as tags como uma lista de strings
        return [tag.name for tag in obj.tags.all()] if obj.tags else []


class ClientSerializer(ModelSerializer):
    user_bio = SerializerMethodField()
    user_name = SerializerMethodField()
    type_user = SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'user',
            'user_name',
            'user_bio',
            'type_user',
            'rating',
            'is_active',
            'created_at',
            'updated_at',
            'contact_info'
        ]

    def get_user_bio(self, obj):
        return obj.user.bio if obj.user else None

    def get_type_user(self, obj):
        return obj.user.profile.get_user_type_display() if obj.user and hasattr(obj.user, 'profile') else None

    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None
