import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProductList from './ProductList';
import Cart from './Cart';
import Receipt from './Receipt';
import '../styles/App.css';

function POS() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showReceipt, setShowReceipt] = useState(false);
  const [lastOrder, setLastOrder] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/products/');
      setProducts(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load products: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.product_id === product.id);
    
    if (existingItem) {
      setCart(cart.map(item =>
        item.product_id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, {
        product_id: product.id,
        name: product.name,
        unit_price: product.price,
        quantity: 1,
        stock: product.stock
      }]);
    }
  };

  const updateCartItem = (product_id, quantity) => {
    if (quantity <= 0) {
      removeFromCart(product_id);
    } else {
      setCart(cart.map(item =>
        item.product_id === product_id
          ? { ...item, quantity }
          : item
      ));
    }
  };

  const removeFromCart = (product_id) => {
    setCart(cart.filter(item => item.product_id !== product_id));
  };

  const calculateTotal = () => {
    return cart.reduce((total, item) => total + (item.unit_price * item.quantity), 0);
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      setError('Cart is empty');
      return;
    }

    try {
      const response = await axios.post('/api/checkout/', {
        items: cart,
        total_amount: calculateTotal()
      });

      setLastOrder(response.data);
      setShowReceipt(true);
      setCart([]);
      setError('');
      
      // Refresh products to update stock
      fetchProducts();
    } catch (err) {
      setError('Checkout failed: ' + (err.response?.data?.error || err.message));
      console.error(err);
    }
  };

  const handleClearReceipt = () => {
    setShowReceipt(false);
    setLastOrder(null);
  };

  if (loading) {
    return <div className="pos-container loading">Loading products...</div>;
  }

  return (
    <div className="pos-container">
      <header className="pos-header">
        <h1>POS System - Flash Sale</h1>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="pos-content">
        <div className="pos-main">
          <ProductList 
            products={products} 
            onAddToCart={addToCart}
          />
        </div>

        <div className="pos-sidebar">
          <Cart 
            items={cart}
            onUpdateItem={updateCartItem}
            onRemoveItem={removeFromCart}
            onCheckout={handleCheckout}
            total={calculateTotal()}
          />
        </div>
      </div>

      {showReceipt && lastOrder && (
        <Receipt 
          order={lastOrder}
          items={cart.length > 0 ? cart : lastOrder.items}
          onClose={handleClearReceipt}
        />
      )}
    </div>
  );
}

export default POS;
