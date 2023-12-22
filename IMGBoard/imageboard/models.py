from django.db import models

# Create your models here.

"""
class User(models.Model):
    username = models.CharField(max_length=20, verbose_name="username", help_text="Username", null=False, blank=False)

    def __str__(self):
        return self.username.__str__()

    class Meta:
        db_table = "Username"
"""


class Board(models.Model):
    title = models.CharField(max_length=25, verbose_name="Board title", help_text="Board's name", null=False,
                             blank=False)
    shortcut = models.CharField(max_length=5, verbose_name="Shortcut", help_text="Shortcut's name", null=True,
                             blank=True)

    def __str__(self):
        return self.title.__str__()

    class Meta:
        db_table = "Board"


class Thread(models.Model):
    title = models.CharField(max_length=50, verbose_name="Thread title", help_text="Thread's name", null=False,
                             blank=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title.__str__()

    class Meta:
        db_table = "Thread"


class Post(models.Model):
    body = models.CharField(max_length=3000, verbose_name="text", help_text="Post content", null=False, blank=False)
    username = models.CharField(max_length=20, verbose_name="username", help_text="Username", null=True, blank=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return self.body.__str__()

    class Meta:
        db_table = "Post"

