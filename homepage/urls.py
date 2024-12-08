from django.urls import path
from . import views as homepage

urlpatterns = [ 
    path('', homepage.homepage_index, name="homepage_index"),
    path('cadastro/', homepage.homepage_cadastro, name="homepage_cadastro"),
    path('sair/', homepage.homepage_logout, name="sair"),
    path('forum/', homepage.homepage_forum, name="forum"),
    path('forum/pergunta/<int:pergunta_id>', homepage.homepage_forum_perguntas, name="forum_pergunta"),
    path('forum/resposta/<int:pergunta_id>', homepage.homepage_forum_reposta, name="forum_resposta")
]