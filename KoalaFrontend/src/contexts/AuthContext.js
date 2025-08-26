import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [tokens, setTokens] = useState(() => {
        const storedTokens = localStorage.getItem('auth_tokens');
        return storedTokens ? JSON.parse(storedTokens) : null;
    });

    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        return !!localStorage.getItem('auth_tokens');
    });

    const [role, setRole] = useState(() => {
        const storedRole = localStorage.getItem('user_role');
        if (storedRole) {
            return storedRole;
        }

        const storedTokens = localStorage.getItem('auth_tokens');
        if (storedTokens) {
            const decodedToken = jwtDecode(JSON.parse(storedTokens).access);
            return decodedToken.role;
        }

        return null;
    });

    useEffect(() => {
        if (tokens) {
            localStorage.setItem('auth_tokens', JSON.stringify(tokens));
            setIsAuthenticated(true);
        } else {
            localStorage.removeItem('auth_tokens');
            setIsAuthenticated(false);
        }
    }, [tokens]);

    const login = (newTokens) => {
        const decodedToken = jwtDecode(newTokens.access);
        const userRole = decodedToken.role;

        setTokens(newTokens);
        setRole(userRole);
        localStorage.setItem('auth_tokens', JSON.stringify(newTokens));
        localStorage.setItem('user_role', userRole);
    };

    const logout = () => {
        setTokens(null);
        setIsAuthenticated(false);
        setRole(null);
        localStorage.removeItem('auth_tokens');
        localStorage.removeItem('user_role');
    };

    return (
        <AuthContext.Provider value={{ tokens, isAuthenticated, role, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};