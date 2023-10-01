from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category
    

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    answer = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.question