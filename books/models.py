from django.db import models
from django.contrib.auth.models import User

class BookIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_number = models.CharField(max_length=20)
    book_name = models.CharField(max_length=100)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_name} - {self.user.username}"