from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout

# Create your views here.
def homepage_index(request):
    return render(request, 'homepage/index.html')

def homepage_cadastro(request):
    return render(request, 'homepage/cadastro.html')

def homepage_logout(request):
    if not request.user.is_authenticated:
        return redirect('homepage_index')
    
    return redirect('login')


def homepage_forum(request):
    # TODO: Implementar a listagem das perguntas
    # - Tabela contendo as colunas: ID | Pergunta | Cadastrado por | Ver
    # Obs: Ver é a coluna com o link para ir para as respostas
    perguntas = []
    return render(request, 'homepage/forum.html', {
        "perguntas": perguntas
    })

def homepage_forum_perguntas(request, pergunta_id):
    # TODO: Implementar o detalhe da pergunta e suas respostas
    # - Pergunta no topo com botão de Responder
    # - Listas de respostas
    pergunta = {}
    respostas = []
    return render(request, 'homepage/forum.html', {
        "pergunta": pergunta,
        "respostas": respostas
    })

def homepage_forum_reposta(request, pergunta_id):
    # TODO: Criar formulário para responder a pergunta
    return render(request, 'homepage/forum.html', {})