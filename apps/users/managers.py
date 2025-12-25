from django.db import models

class LectoresManagers(models.Manager):
    
    def active_since(self, year):
        return self.filter(joined_at__year=year)