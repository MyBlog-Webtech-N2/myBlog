from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from collections import Counter

from authenticate.models import CustomUser


class Article(models.Model):
    title = models.CharField(max_length=90)
    content = models.TextField(null=True)
    icon = models.ImageField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - Auteur: {self.author.username}"

    def time_since_created(self):
        delta = timezone.now() - self.date

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} {'day' if days == 1 else 'days'}"
        elif hours > 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'}"
        elif minutes > 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"
        else:
            return f"{seconds} {'second' if seconds == 1 else 'seconds'}"

    def calculate_average(self):
        comments = self.comments.all()
        images = [
            "very-cool.png",
            'cool.png',
            'good.png',
            'not-bad.png',
            'bad.png'
        ]
        if comments.count() < 1:
            return {'total_comments': 0, 'average_total': 0,
                    'percentages_array': [None, None, None, None, None], 'average_image': None, 'images': images}
        total_comments = comments.count()
        star_counts = Counter(comment.star for comment in comments)

        percentages_array = [
            {'stars': star_counts[star], 'percentage': round((star_counts[star] / total_comments) * 100)} for star
            in range(5, 0, -1)]
        total_stars = sum(comment.star for comment in comments)
        average = total_stars / total_comments
        return {'total_comments': total_comments, 'average_total': round(average), 'images': images,
                'percentages_array': percentages_array, 'average_image': determine_average_image(average)}


def determine_average_image(average):
    images = [
        {'threshold': 4, 'image': 'very-cool.png'},
        {'threshold': 3, 'image': 'cool.png'},
        {'threshold': 2, 'image': 'good.png'},
        {'threshold': 1, 'image': 'not-bad.png'},
        {'threshold': 0, 'image': 'bad.png'}
    ]

    for img in images:
        if average >= img['threshold']:
            return img['image']

    return 'bad.png'


@receiver(pre_save, sender=Article)
def set_author_on_save(sender, instance, **kwargs):
    if not instance.author:
        instance.author = CustomUser.objects.get(pk=instance.author_id)
