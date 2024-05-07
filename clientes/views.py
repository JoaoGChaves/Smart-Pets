from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pet
import re
from django.core import serializers
import json

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
    pets_json=json.loads(serializers.serialize('json', pets))
    pets_json=[{'fields': pet['fields'], 'id': pet['pk']} for pet in pets_json]
    data ={'cliente': cliente_json, 'pets': pets_json}
    return JsonResponse(data)
