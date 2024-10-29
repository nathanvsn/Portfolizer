# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from .services import EmailService
import logging

logger = logging.getLogger(__name__)

User = get_user_model()
@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    """
    Signal para enviar email de verificação quando um novo usuário é criado
    """
    if created and not instance.is_email_verified:
        try:
            # Gera token seguro para verificação
            signer = Signer()
            token = signer.sign(instance.email)
            
            # Envia o email de verificação
            EmailService.send_verification_email(instance, token)
        except Exception as e:
            # Log do erro para monitoramento
            logger.error(f"Erro ao enviar email de verificação para {instance.email}: {str(e)}")
