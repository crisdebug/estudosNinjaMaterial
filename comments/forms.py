from django import forms
from comments.models import ComentarioModel
from django_comments.forms import CommentDetailsForm

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils import timezone
from django.conf import settings

class Comentario(CommentDetailsForm):
    def __init__(self, *args, **kwargs):
        super(Comentario, self).__init__(*args, **kwargs)
        self.fields.pop('name')
        self.fields.pop('email')
        self.fields.pop('url')

    def get_comment_create_data(self, site_id=None):
        """
        Returns the dict of data to be used to create a comment. Subclasses in
        custom comment apps that override get_comment_model can override this
        method to add extra fields onto a custom comment model.
        """
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_text(self.target_object._get_pk_val()),
            comment=self.cleaned_data["comment"],
            submit_date=timezone.now(),
            site_id=site_id or getattr(settings, "SITE_ID", None),
            is_public=True,
            is_removed=False,
        )