from custom_auth.models import User
from django.db import models
from taggit.managers import TaggableManager

class UserTypes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Freelancer(UserTypes):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer_profile")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.user.username


class Client(UserTypes):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="works")
    title = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(upload_to="work_images/", blank=True, null=True)
    tags = TaggableManager(blank=True)
    is_per_hour = models.BooleanField(default=False)
    hour_per_week = models.IntegerField(default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.client.name}"


class Proposal(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="proposals")
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name="proposals")
    message = models.TextField()  # Mensagem do freelancer ao se candidatar
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Proposta de valor
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal by {self.freelancer.user.username} for {self.work.title}"


class Review(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.reviewee.username} by {self.reviewer.username}"


class ChatRoom(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name="chat_room")
    is_active = models.BooleanField(default=False)  # Sala ativa apenas quando a proposta é aceita
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom for Proposal {self.proposal.id} - {self.proposal.work.title}"


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in ChatRoom {self.chat_room.id}"
