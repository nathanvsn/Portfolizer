from rest_framework.serializers import ModelSerializer, SerializerMethodField
from portfolios.models import Vote, Project


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['user', 'project', 'created_at']
        read_only_fields = ['created_at']


class ProjectSerializer(ModelSerializer):
    portfolio_user_full_name = SerializerMethodField()
    portfolio_user_username = SerializerMethodField()
    portfolio_user_type = SerializerMethodField()
    tags = SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'portfolio',
            'portfolio_user_full_name',
            'portfolio_user_username',
            'portfolio_user_type',
            'name',
            'img',
            'description',
            'tags',
            'votes',
        ]

    def get_portfolio_user_full_name(self, obj):
        return obj.portfolio.user.get_full_name() if obj.portfolio.user else ''

    def get_portfolio_user_username(self, obj):
        return obj.portfolio.user.username if obj.portfolio.user else ''

    def get_portfolio_user_type(self, obj):
        return obj.portfolio.user.profile.get_user_type_display() if obj.portfolio.user else ''

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()] if obj.tags else []
