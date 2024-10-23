class ResourceService:
    @staticmethod
    def can_upload_more_resources(project):
        user_type = project.portfolio.user.profile.user_type
        if user_type == 'free' and project.resources.count() >= 2:
            return False
        elif user_type == 'pro' and project.resources.count() >= 10:
            return False
        return True
    
    @staticmethod
    def total_storage_used(portfolio):
        total = 0
        for project in portfolio.projects.all():
            total += sum(res.file_size for res in project.resources.all())
        return total
