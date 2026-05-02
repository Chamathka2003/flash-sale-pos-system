import React, { useState } from "react";
import "../styles/App.css";

function ProductList({ products, onAddToCart }) {
  const [selectedCategory, setSelectedCategory] = useState(null);

  const getStockClass = (stock) => {
    if (stock > 50) return "stock-high"; // Dark green
    if (stock >= 20) return "stock-medium"; // Light green
    if (stock >= 10) return "stock-warning"; // Orange/Yellow
    if (stock > 0) return "stock-low"; // Red
    return "stock-empty"; // Out of stock
  };

  // Extract unique categories from products
  const categories = [...new Set(products.map((p) => p.name.split(" ")[0]))];

  // Filter products based on selected category
  const filteredProducts = selectedCategory
    ? products.filter((p) => p.name.includes(selectedCategory))
    : products;

  return (
    <div className="product-list">
      <h2>Products Available</h2>

      {/* Category Filter Section */}
      <div className="category-filter">
        <button
          className={`category-badge ${selectedCategory === null ? "active" : ""}`}
          onClick={() => setSelectedCategory(null)}
        >
          All
        </button>
        {categories.map((category) => (
          <button
            key={category}
            className={`category-badge ${selectedCategory === category ? "active" : ""}`}
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="products-grid">
        {filteredProducts.map((product) => (
          <div
            key={product.id}
            className={`product-card ${getStockClass(product.stock)}`}
          >
            <h3>{product.name}</h3>
            <div className="product-price">
              ${parseFloat(product.price).toFixed(2)}
            </div>
            <div className={`product-stock ${getStockClass(product.stock)}`}>
              Stock: {product.stock}
            </div>
            <button
              className={`btn-add-to-cart ${getStockClass(product.stock)}`}
              onClick={() => onAddToCart(product)}
              disabled={product.stock === 0}
            >
              {product.stock > 0 ? "Add to Cart" : "Out of Stock"}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;
