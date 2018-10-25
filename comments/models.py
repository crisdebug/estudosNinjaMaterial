from django.db import models
from django_comments.abstracts import BaseCommentAbstractModel

class ComentarioModel(BaseCommentAbstractModel):
    comment = models.CharField(max_length=300)