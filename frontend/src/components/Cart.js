import React from "react";
import "../styles/App.css";

function Cart({ items, onUpdateItem, onRemoveItem, onCheckout, total }) {
  return (
    <div className="cart-container">
      <h2>Shopping Cart</h2>

      {items.length === 0 ? (
        <p className="empty-cart">Cart is empty</p>
      ) : (
        <>
          <div className="cart-header">
            <div className="header-description">DESCRIPTION</div>
            <div className="header-qty">QTY</div>
            <div className="header-price">PRICE</div>
          </div>
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.product_id} className="cart-item">
                <div className="cart-item-info">
                  <div className="cart-item-name">{item.name}</div>
                  <button
                    onClick={() => onRemoveItem(item.product_id)}
                    className="btn-remove"
                    title="Remove item"
                  >
                    ×
                  </button>
                </div>

                <div className="cart-item-quantity">
                  <button
                    onClick={() =>
                      onUpdateItem(item.product_id, item.quantity - 1)
                    }
                    className="qty-btn"
                  >
                    -
                  </button>
                  <span style={{ textAlign: "center", minWidth: "30px" }}>
                    {item.quantity}
                  </span>
                  <button
                    onClick={() =>
                      onUpdateItem(item.product_id, item.quantity + 1)
                    }
                    className="qty-btn"
                  >
                    +
                  </button>
                </div>

                <div className="cart-item-subtotal">
                  ${(item.unit_price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          <div className="cart-total">
            <strong>Grand Total: ${total.toFixed(2)}</strong>
          </div>

          <button onClick={onCheckout} className="btn-checkout">
            Checkout
          </button>
        </>
      )}
    </div>
  );
}

export default Cart;
