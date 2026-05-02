import React from "react";
import "../styles/App.css";

function Receipt({ order, items, onClose }) {
  const receiptDate = new Date().toLocaleString();

  return (
    <div className="receipt-overlay" onClick={onClose}>
      <div className="receipt-modal" onClick={(e) => e.stopPropagation()}>
        <div className="receipt-container thermal-paper">
          <div className="receipt-header">
            <h1>FLASH SALE POS</h1>
            <p>Receipt</p>
          </div>

          <div className="receipt-separator">
            - - - - - - - - - - - - - - - - -
          </div>

          <div className="receipt-info">
            <div className="info-line">
              <span>Order #:</span>
              <span className="mono">{order.order_number}</span>
            </div>
            <div className="info-line">
              <span>Date/Time:</span>
              <span className="mono">{receiptDate}</span>
            </div>
          </div>

          <div className="receipt-separator">
            - - - - - - - - - - - - - - - - -
          </div>

          <div className="receipt-items">
            <div className="item-header">
              <span className="item-desc">DESCRIPTION</span>
              <span className="item-qty">QTY</span>
              <span className="item-price">PRICE</span>
            </div>
            <div className="receipt-separator">
              - - - - - - - - - - - - - - - - -
            </div>

            {items && items.length > 0 ? (
              items.map((item, index) => (
                <div key={index} className="receipt-item">
                  <div className="item-line">
                    <span className="item-desc">
                      {item.name || item.product_name}
                    </span>
                    <span className="item-qty">{item.quantity}</span>
                    <span className="item-price">
                      ${parseFloat(item.unit_price).toFixed(2)}
                    </span>
                  </div>
                  <div className="item-subtotal">
                    Subtotal: ${(item.quantity * item.unit_price).toFixed(2)}
                  </div>
                </div>
              ))
            ) : (
              <div className="receipt-item">
                <p style={{ fontSize: "10px", color: "#999" }}>
                  No items found
                </p>
              </div>
            )}
          </div>

          <div className="receipt-separator">
            = = = = = = = = = = = = = = = = =
          </div>

          <div className="receipt-total">
            <div className="total-line">
              <span>TOTAL:</span>
              <span className="total-amount">
                ${parseFloat(order.total_amount).toFixed(2)}
              </span>
            </div>
          </div>

          <div className="receipt-separator">
            - - - - - - - - - - - - - - - - -
          </div>

          <div className="receipt-footer">
            <p>Thank you for your purchase!</p>
            <p className="status">Status: {order.status.toUpperCase()}</p>
          </div>

          <div className="receipt-separator">
            - - - - - - - - - - - - - - - - -
          </div>

          <button onClick={onClose} className="btn-close-receipt">
            Close Receipt
          </button>
        </div>
      </div>
    </div>
  );
}

export default Receipt;
