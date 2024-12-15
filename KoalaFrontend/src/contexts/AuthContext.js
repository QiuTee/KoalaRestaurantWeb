import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [tokens, setTokens] = useState(() => {
        const storedTokens = localStorage.getItem('auth_tokens');
        return storedTokens ? JSON.parse(storedTokens) : null;
    });
    
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        return !!localStorage.getItem('auth_tokens');
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
        setTokens(newTokens);
        setIsAuthenticated(true);
    };

    const logout = () => {
        setTokens(null);
        setIsAuthenticated(false);
        localStorage.removeItem('auth_tokens');
    };

    return (
        <AuthContext.Provider value={{ tokens, isAuthenticated, login, logout }}>
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
