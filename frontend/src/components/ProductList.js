import React from 'react';
import '../styles/App.css';

function ProductList({ products, onAddToCart }) {
  return (
    <div className="product-list">
      <h2>Products Available</h2>
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <div className="product-price">${parseFloat(product.price).toFixed(2)}</div>
            <div className={`product-stock ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
              Stock: {product.stock}
            </div>
            <button 
              className="btn-add-to-cart"
              onClick={() => onAddToCart(product)}
              disabled={product.stock === 0}
            >
              {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;
