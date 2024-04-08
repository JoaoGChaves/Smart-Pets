function add_pet(){

    container = document.getElementById('form-pet')

    html = "<br> <div class='row'> <div class='col-md'> <input type='text' placeholder='pet' class='form-control' name='pet'> </div> <div class='col-md'> <input type='text' placeholder='raca' class='form-control' name='raca'> </div> <div class='col-md'> <input type='number' placeholder='idade' class='form-control' name='idade'> </div> </div>"

    container.innerHTML += html
}
