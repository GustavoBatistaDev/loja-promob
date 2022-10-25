from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Produto, Categoria


def home(request):

    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'produtos': produtos,
                                        'carrinho': len(request.session['carrinho']),
                                        'categorias': categorias,
                                        })


def categoria(request, categoria_id):
    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
    produtos = Produto.objects.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'produtos': produtos,
                                        'carrinho': len(request.session['carrinho']),
                                        'categorias': categorias,
                                        })


def produto(request, id):
    if not request.session.get('carrinho'):
        request.session['carrinho'] = []
        request.session.save()
        
    erro = request.GET.get('erro')
    produto = get_object_or_404(Produto, id=id)
    categorias = Categoria.objects.all()
    return render(request, 'produto.html', {'produto': produto, 
                                            'carrinho': len(request.session['carrinho']),
                                            'categorias': categorias,
                                            'erro': erro})


def add_carrinho(request):
    if not request.session['carrinho']:
        request.session['carrinho'] = []
        request.session.save()

    x = request.POST


    id = int(x['id'])
    
    preco_total = Produto.objects.filter(id=id)[0].preco


    preco_total = preco_total * int(x['quantidade'])
    data = {'id_produto': int(x['id']),
            'observacoes': x['observacoes'],
            'preco': preco_total,
            'quantidade': x['quantidade']}

    request.session['carrinho'].append(data)
    request.session.save()
    return redirect(f'/ver_carrinho')


def ver_carrinho(request):
    categorias = Categoria.objects.all()

    dados_motrar = []

    for y, i in enumerate(request.session['carrinho']): 
        prod = get_object_or_404(Produto, id=i['id_produto'])

     
        var =   {'imagem': prod.img.url,
            'nome': prod.nome_produto,
            'quantidade': i['quantidade'],
            'preco': i['preco'],
            'id': i['id_produto'],
            'session_id': y
       
            
            }


        dados_motrar.append(var)
          
 
    total = sum([float(i['preco']) for i in request.session['carrinho']])


    return render(request, 'carrinho.html', {'dados': dados_motrar,
                                             'total': total,
                                             'carrinho': len(request.session['carrinho']),
                                             'categorias': categorias,
                                             })


def remover_carrinho(request, session_id):
    request.session['carrinho'].pop(session_id)
    request.session.save()
    return redirect('/ver_carrinho')