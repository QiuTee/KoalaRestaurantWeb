import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from 'react-toastify';
import submission from "../../utils/submission";
import { jwtDecode } from "jwt-decode";

const Payment = ({ cartItems, totalAmount, onClose }) => {
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const navigate = useNavigate();

  const handlePayment = async () => {
    try {
      console.log("Starting payment process...");
      const token = localStorage.getItem('authToken');
      if (!token) {
        toast.error('Please login to pay!');
        navigate('/login');
        return;
      }

      const decoded = jwtDecode(token);
      const customerId = decoded?.user_id;

      console.log("Sending payment request...", {
        customerId,
        paymentMethod,
        totalAmount
      });

      const response = await submission(
        `app/payment/?customer=${customerId}`,
        'post',
        {
          payment_method: paymentMethod,
          total_amount: totalAmount,
          cart_items: cartItems.map(item => ({
            menu_item: item.id,
            quantity: item.quantity,
            price: item.price
          }))
        },
        {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        }
      );

      console.log("Payment response:", response);

      if (response && response.status === '200') {
        toast.success('Payment successfully!');
        onClose();
        setTimeout(() => {
          navigate('/order-history');
        }, 2000);
      } else {
        toast.error('Payment failed! Please try again.');
      }
    } catch (error) {
      console.error('Payment error:', error);
      toast.error('An error occurred during payment!');
    }
  };

  return (
    <div className="space-y-6">
      {/* Thông tin đơn hàng */}
      <div className="space-y-4">
        <h3 className="font-semibold">Order Information</h3>
        {cartItems?.map((item, index) => (
          <div key={index} className="flex justify-between">
            <span>{item.food_name} x {item.quantity}</span>
            <span>{item.price * item.quantity} VND</span>
          </div>
        ))}
        <div className="border-t pt-4">
          <div className="flex justify-between font-bold">
            <span>Total:</span>
            <span>{totalAmount} VND</span>
          </div>
        </div>
      </div>

      {/* Phương thức thanh toán */}
      <div className="space-y-4">
        <h3 className="font-semibold">Phương thức thanh toán</h3>
        <div className="space-y-2">
          <label className="flex items-center space-x-3">
            <input
              type="radio"
              value="cash"
              checked={paymentMethod === "cash"}
              onChange={(e) => setPaymentMethod(e.target.value)}
            />
            <span>Cash</span>
          </label>
          <label className="flex items-center space-x-3">
            <input
              type="radio"
              value="bank"
              checked={paymentMethod === "bank"}
              onChange={(e) => setPaymentMethod(e.target.value)}
            />
            <span>Bank Transfer</span>
          </label>
        </div>
      </div>

      {/* Buttons */}
      <div className="flex justify-end space-x-4">
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          onClick={handlePayment}
          className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600"
        >
          Confirm Payment
        </button>
      </div>
    </div>
  );
};

export default Payment;
