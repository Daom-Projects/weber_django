// frontend/src/App.jsx
import { useState, useEffect } from 'react';

// Un componente simple para mostrar una tarjeta de producto
function ProductoCard({ producto }) {
  return (
    <div className="col-md-4 mb-4">
      <div className="card">
        <div className="card-body">
          <h5 className="card-title">{producto.nombre}</h5>
          <h6 className="card-subtitle mb-2 text-muted">SKU: {producto.codigo || 'N/A'}</h6>
          <p className="card-text">{producto.descripcion?.substring(0, 100)}...</p>
          <p className="card-text"><strong>Stock:</strong> {producto.stock}</p>
        </div>
      </div>
    </div>
  );
}

function App() {
  // Estado para guardar la lista de productos y el estado de carga
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // useEffect se ejecuta cuando el componente se monta por primera vez
  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/productos/');
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        setProductos(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProductos();
  }, []); // El array vacío [] asegura que se ejecute solo una vez

  // Lógica de renderizado condicional
  if (loading) {
    return <p>Cargando productos...</p>;
  }

  if (error) {
    return <p className="text-danger">Error al cargar los productos: {error}</p>;
  }

  return (
    <div>
      <h1>Lista de Productos (Renderizada con React)</h1>
      <p className="text-muted">Esta página es una SPA de React que consume la API de Django.</p>
      <div className="row">
        {productos.map(producto => (
          <ProductoCard key={producto.id} producto={producto} />
        ))}
      </div>
    </div>
  );
}

export default App;