import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        """
        Envia email de verificação para um novo usuário
        
        Args:
            user: Instância do modelo User
            token: Token de verificação gerado
        
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrário
        """
        try:
            # Validação dos dados
            if not user.email:
                raise ValidationError("Email do usuário não fornecido")
            if not token:
                raise ValidationError("Token de verificação não fornecido")

            # Construção do link de verificação
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
            
            # Contexto para o template
            context = {
                'user': user,
                'link': verification_url
            }
            
            # Renderiza o template HTML
            html_content = render_to_string('emails/verification_email.html', context)
            
            # Envia o email
            sent = send_mail(
                subject="Confirme seu email - Portfolizer",
                message="",  # Versão plain text (opcional)
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False
            )
            
            if sent:
                logger.info(f"Email de verificação enviado com sucesso para {user.email}")
                return True
            else:
                logger.warning(f"Falha ao enviar email de verificação para {user.email}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar email de verificação: {str(e)}")
            raise