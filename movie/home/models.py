from django.db import models

# Create your models here.
class Review(models.Model):
    critic_name = models.CharField( ("name") ,max_length=122)
    movie_name=   models.CharField( ("name") ,max_length=122)
    review_Score = models.FloatField( ("desc"))
    review_content  = models.CharField( ("name") ,max_length=122)
    
    def __str__(self):
        return self.name



