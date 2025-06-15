from django.apps import AppConfig
  
class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging' 
    def ready(self):
        import messaging.signals  # Ensure this matches your app name


