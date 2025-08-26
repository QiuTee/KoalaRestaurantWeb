import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = ({ children, requiredRole }) => {
    const { isAuthenticated, tokens, role } = useAuth();

    // Log the values for debugging
    console.log('isAuthenticated:', isAuthenticated);
    console.log('tokens:', tokens);
    console.log('role:', role);

    if (tokens === undefined) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated || !tokens) {
        return <Navigate to="/manager-login" replace />;
    }

    if (requiredRole && role !== requiredRole) {
        return <Navigate to="/manager-login" replace />;
    }

    return children;
};

export default ProtectedRoute;