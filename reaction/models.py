from django.db import models

from blog.models import Article, CustomUser


# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    star = models.IntegerField(default=5)  # 1 2 3 4 5
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image(self):
        images = [
            'bad.png',
            'not-bad.png',
            'good.png',
            'cool.png',
            "very-cool.png"
        ]
        return images[self.star - 1]
