function add_pet(){

    container = document.getElementById('form-pet')

    html = "<br> <div class='row'> <div class='col-md'> <input type='text' placeholder='pet' class='form-control' name='pet'> </div> <div class='col-md'> <input type='text' placeholder='raca' class='form-control' name='raca'> </div> <div class='col-md'> <input type='number' placeholder='idade' class='form-control' name='idade'> </div> </div>"

    container.innerHTML += html
}
 function exibir_form(tipo){
    add_cliente=document.getElementById('adicionar-cliente')
    att_cliente=document.getElementById('att_cliente')

    if(tipo=="1"){
        att_cliente.style.display ="none"
        add_cliente.style.display ="block"
    }else if(tipo=="2"){
        add_cliente.style.display ="none"
        att_cliente.style.display ="block"
    }
 }

 function dados_cliente(){
    cliente= document.getElementById('cliente-select')
    csrf_token= document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente=cliente.value

    data= new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/", {
        method:"POST", 
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function(result){
        return result.json()
    }).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'
        nome=document.getElementById('nome')
        nome.value=data['cliente']['nome']

        sobrenome=document.getElementById('sobrenome')
        sobrenome.value=data['cliente']['sobrenome']

        email=document.getElementById('email')
        email.value=data['cliente']['email']

        cpf=document.getElementById('cpf')
        cpf.value=data['cliente']['cpf']

        div_pets=document.getElementById('pets')
        div_pets.innerHTML=""

        for(i=0;i<data['pets'].length; i++){
            console.log(data['pets'][i]['fields']['carro'])
            div_pets.innerHTML += "<form action='' method''>\
                <div class='row'>\
                    <div class='col-md'>\
                        <input class='form-control' type='text' name='pet' value='"  +data['pets'][i]['fields']['carro']+ "'>\
                    </div>\
                    <div class='col-md'>\
                        <input class='form-control' type='text' name='raca' value='"  +data['pets'][i]['fields']['raca']+ "'>\
                    </div>\
                    <div class='col-md'>\
                        <input class='form-control' type='text' name='idade' value='"  +data['pets'][i]['fields']['idade']+ "'>\
                    </div>\
                    <div class='col-md'>\
                        <input class='btn btn-success' type='submit'>\
                    </div>\
                </div><br>"
        }
    })
 }      