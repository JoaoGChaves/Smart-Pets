from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pet
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

def clientes(request):  
    if request.method== "GET":
        clientes_list=Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list}) 
    elif request.method=="POST":
        nome=request.POST.get('nome')
        sobrenome=request.POST.get('sobrenome')
        email=request.POST.get('email')
        cpf=request.POST.get('cpf')
        pets=request.POST.getlist('pet')
        racas=request.POST.getlist('raca')
        idades=request.POST.getlist('idade')

        cliente=Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'pets': zip(pets, racas, idades)})
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'pets': zip(pets, racas, idades)})
        
        cliente=Cliente(
            nome= nome,
            sobrenome= sobrenome,
            email=email,
            cpf=cpf,
        )
        cliente.save()
        for carro, raca, idade in zip(pets, racas, idades):
            pat= Pet(carro=carro, raca=raca, idade=idade, cliente=cliente)
            pat.save()
        return HttpResponse('teste')
    

def att_cliente(request):
    id_cliente=request.POST.get('id_cliente')

    cliente=Cliente.objects.filter(id=id_cliente)
    pets=Pet.objects.filter(cliente=cliente[0])
    cliente_json=json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id=json.loads(serializers.serialize('json', cliente))[0]['pk']
    pets_json=json.loads(serializers.serialize('json', pets))
    pets_json=[{'fields': pet['fields'], 'id': pet['pk']} for pet in pets_json]
    data ={'cliente': cliente_json, 'pets': pets_json, 'cliente_id':cliente_id}
    return JsonResponse(data)

@csrf_exempt
def update_pet(request, id):
    nome_pet=request.POST.get('pet')
    raca= request.POST.get('raca')
    idade= request.POST.get('idade')

    pet=Pet.objects.get(id=id)
    pet.pet=nome_pet
    pet.raca=raca
    pet.idade=idade
    return HttpResponse("Dados alterados com sucesso")

def excluir_pet(request, id):
    try:
        pet=Pet.objects.get(id=id)
        pet.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')
    except:
        #TODO: Exibir mensagem de erro
        return redirect(reverse('clientes')+f'?aba=att_cliente&id_cliente={id}')
    
def update_cliente(request, id):
    body=json.loads(request.body)
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']

    cliente=get_object_or_404(Cliente, id=id)
    try:
        cliente.nome=nome
        cliente.sobrenome=sobrenome
        cliente.email=email
        cliente.cpf=cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf':cpf})
    except:
        return JsonResponse({'status': '500'})
