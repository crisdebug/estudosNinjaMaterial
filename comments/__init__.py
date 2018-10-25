def get_form():
    from comments.forms import Comentario
    return Comentario

def get_form_target():
    from django.urls import reverse
    return reverse('postar-comentario')

