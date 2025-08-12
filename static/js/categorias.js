document.addEventListener('DOMContentLoaded', ()=> {
    // Obtiene los elementos del DOM
    const select = document.getElementById('category_select');
    const selectedList = document.getElementById('selected_categories');
    const hiddenInputs = document.getElementById('hidden_category_inputs');

    // Se obtiene mediante querySelector para que devuelva 0 en caso que este vacio, asi
    // funciona tanto para crear un post (devuelve 0) o para editarlo (devuelve 1, 2 o 3)
    const categorias_existentes = document.querySelectorAll('#selected_categories > div');

    // Se asegura de que existan (para evitar fallos)
    if (!select || !selectedList || !hiddenInputs) return;

    const ids = [] // Array con las ids de las categorias para manejar la logica interna
    // (no se envia al back)

    // Funcion para renderizar tanto las categorias seleccionadas como el manejo de la logica interna
    const crear_div_categoria = (name,id)=> {
    
        // Crea el div para renderizar dinamico las categorias seleccionadas
        const card = document.createElement('div');
        card.classList.add("list-group-item","d-inline-flex","align-items-center","justify-content-between","mx-2", "rounded-pill");
        const p = document.createElement('p');
        p.classList.add("mb-0","mx-1");
        p.textContent = name + " ";

        // Crea el boton para remover la categoria seleccionada
        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'x';
        removeBtn.classList.add("btn","btn-danger","rounded-circle","py-0","px-2","align-items-center","justify-content-center");
        removeBtn.addEventListener('click', ()=> {
            selectedList.removeChild(card);
            hiddenInputs.removeChild(hiddenInput); // Borra tambien el hiddenInput
            index = ids.indexOf(id);
            ids.splice(index,1); // Borra el id de la lista para el manejo interno
        });

        // Agrega los elementos texto y boton al div
        card.appendChild(p);
        card.appendChild(removeBtn);
        selectedList.appendChild(card);

        // Crea un input de tipo oculto ('hidden') que luego flask recibira como una lista bajo
        // el name 'categories', sea que reciba 1, 2 o 3 elementos en esa lista.
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'categories';
        hiddenInput.value = id;
        hiddenInputs.appendChild(hiddenInput);
    }

    // Esta condicion permite recibir las categorias existentes en caso que hubiera
    if (categorias_existentes.length > 0){
        categorias_existentes.forEach(categoria => {
            const name = categoria.querySelector('p').textContent;
            const id = categoria.querySelector('input').value;
            ids.push(id);
            crear_div_categoria(name,id);
            selectedList.removeChild(categoria)
        });
    }

    // Maneja el selector de categorias
    select.addEventListener('change', ()=> {
        const selectedOption = select.options[select.selectedIndex];
        const id = selectedOption.value;
        const name = selectedOption.text;

        // Evita que pueda seleccionar dos veces la misma categoria
        if (!id || ids.includes(id) || id === "") {
            return;
        };

        // Limita la seleccion a 3 categorias
        if (ids.length > 2) {
            return;
        }

        ids.push(id);

        // Crea el div y la logica con la categoria seleccionada
        crear_div_categoria(name, id);

    });

})