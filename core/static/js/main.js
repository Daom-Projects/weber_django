// core/static/js/main.js

// Nos aseguramos de que el script se ejecute solo cuando el DOM esté completamente cargado.
document.addEventListener('DOMContentLoaded', () => {
    const appContainer = document.getElementById('app');
    const API_URL = 'http://127.0.0.1:8000/api/productos/?format=json';

    // Función para renderizar los productos en el HTML
    const renderProductos = (productos) => {
        // Limpiamos el contenedor
        appContainer.innerHTML = '';

        if (productos.length === 0) {
            appContainer.innerHTML = '<p>No se encontraron productos.</p>';
            return;
        }

        // Creamos una tarjeta para cada producto
        productos.forEach(producto => {
            const card = document.createElement('div');
            card.className = 'col-md-4 mb-4';

            card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${producto.nombre}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">SKU: ${producto.codigo || 'N/A'}</h6>
                        <p class="card-text">${producto.descripcion.substring(0, 100)}...</p>
                        <p class="card-text"><strong>Stock:</strong> ${producto.stock}</p>
                    </div>
                </div>
            `;
            appContainer.appendChild(card);
        });
    };

    // Función para obtener los productos de la API usando async/await
    const fetchProductos = async () => {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            const data = await response.json();
            renderProductos(data);
        } catch (error) {
            appContainer.innerHTML = `<p class="text-danger">Error al cargar los productos: ${error.message}</p>`;
            console.error('Error fetching productos:', error);
        }
    };

    // Llamamos a la función para cargar los productos al iniciar.
    fetchProductos();
});