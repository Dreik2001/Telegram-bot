from django.db import models

# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='User ID in social network',
        unique=True,
    )
    name = models.TextField(
        verbose_name='User name',
    )
   

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text',
    )

    created_at = models.DateTimeField(
        verbose_name='Time getting',
        auto_now_add=True,
    )



    def __str__(self):
        return f'Message {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages_id'


# class Comment(models.Model):
# 	pass
# 	post = models.ForeignKey(Post, related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField(max_length=200, blank=True)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     # manually deactivate inappropriate comments from admin site
#     active = models.BooleanField(default=True)
#     parent = models
