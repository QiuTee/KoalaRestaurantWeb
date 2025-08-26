import React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const OrderButton = ({ cartItems, calculateGrandTotal, setShowPayment }) => {
  const navigate = useNavigate();

  const handleOrder = async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) {
        toast.error('Please login to place an order!');
        navigate('/login');
        return;
      }

      // Mở modal payment
      setShowPayment(true);

    } catch (error) {
      console.error('Order error:', error);
      toast.error('An error occurred!');
    }
  };

  return (
    <button
      onClick={handleOrder}
      disabled={!cartItems || cartItems.length === 0}
      className={`
        w-full py-3 mt-4 
        font-medium text-white 
        bg-orange-500 hover:bg-orange-600 
        rounded-lg transition-colors
        ${(!cartItems || cartItems.length === 0) ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      Place an order
    </button>
  );
};

export default OrderButton;
