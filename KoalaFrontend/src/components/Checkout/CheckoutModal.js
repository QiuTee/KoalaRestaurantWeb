import React from 'react';
import OrderButton from '../Button/OrderButton';

const CheckoutModal = ({ cartItems, calculateTotalPrice, calculateGrandTotal, setShowPayment }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Total</h2>
      
      <div className="space-y-4 mb-4">
        {cartItems.map((item, index) => (
          <div key={index} className="flex justify-between">
            <span>{item.food_name} x {item.quantity}</span>
            <span>{calculateTotalPrice(item)} VND</span>
          </div>
        ))}
      </div>

      <div className="border-t pt-4">
        <div className="flex justify-between font-bold">
          <span>Total:</span>
          <span>{calculateGrandTotal()} VND</span>
        </div>
      </div>

      <OrderButton 
        cartItems={cartItems} 
        calculateGrandTotal={calculateGrandTotal}
        setShowPayment={setShowPayment}
      />
    </div>
  );
};

export default CheckoutModal;
