from django.db import models

class Cliente(models.Model):
    nome=models.CharField(max_length=50)
    sobrenome=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    cpf=models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.nome
    
class Pet(models.Model) :
    carro=models.CharField(max_length=50)
    raca=models.CharField(max_length=50)
    idade=models.IntegerField()
    cliente=models.ForeignKey(Cliente, on_delete=models.CASCADE)
    banhos=models.IntegerField(default=0)
    tosas=models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.carro
