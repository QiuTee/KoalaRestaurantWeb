import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { EyeIcon, EyeOffIcon } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import submission from '../../utils/submission';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ReCAPTCHA from 'react-google-recaptcha';  // Thêm ReCAPTCHA

const ManagerLogin = () => {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showCaptcha, setShowCaptcha] = useState(false);  
    const [captchaToken, setCaptchaToken] = useState('');    

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleTogglePassword = () => {
        setShowPassword(!showPassword);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        const loginData = {
            email: formData.email,
            password: formData.password,
            recaptcha: showCaptcha ? captchaToken : '',  // Thêm token CAPTCHA nếu có
        };

        try {
            const response = await submission('authentication/manager/login/', 'post', loginData);
            
            if (response && response.status === "200") {
                // Lấy token từ response.data
                login({ 
                    access: response.data.access, 
                    refresh: response.data.refresh 
                });

                // Hiển thị thông báo thành công
                toast.success('Admin login successful!', {
                    position: "top-right",
                    autoClose: 2000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                });

                setTimeout(() => {
                    navigate('/admin-dashboard');
                }, 2000);
            }else if (response.status === "400"){
                toast.error(response.message, {
                    position: "top-right",
                    autoClose: 2000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                });
            } 
            else {
                toast.error('Invalid login information');
            }
        } catch (error) {
            console.error('Login error', error);
            if (error.response?.status === 429) {
                setShowCaptcha(true);
                setError('Too many login attempts. Please complete the CAPTCHA.');
            } else {
                setError(error.response?.data?.detail || 'An error has occurred. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto p-8 bg-white shadow-lg rounded-lg">
            <ToastContainer />
            <h2 className="text-2xl font-bold text-center mb-2">Đăng nhập quản trị</h2>
            {error && <p className="text-center text-red-500 mb-2">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="email" className="block text-sm font-medium mb-1">Email</label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        required
                        placeholder="name@example.com"
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block text-sm font-medium mb-1">Password</label>
                    <div className="relative">
                        <input
                            type={showPassword ? 'text' : 'password'}
                            name="password"
                            id="password"
                            required
                            placeholder="••••••••"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <button
                            type="button"
                            onClick={handleTogglePassword}
                            className="absolute inset-y-0 right-2 flex items-center text-gray-500"
                        >
                            {showPassword ? <EyeOffIcon className="h-5 w-5" /> : <EyeIcon className="h-5 w-5" />}
                        </button>
                    </div>
                </div>

                {/* CAPTCHA */}
                {showCaptcha && (
                    <div className="mb-4">
                        <ReCAPTCHA
                            sitekey="6LeZM5UqAAAAAMxEapzr-UbNvcupx_wV6vWf_zdI"
                            onChange={(token) => setCaptchaToken(token)}
                        />
                    </div>
                )}

                <button 
                    type="submit" 
                    className="w-full py-2 px-4 bg-black text-white rounded-md hover:bg-gray-800 transition duration-200"
                    disabled={loading}
                >
                    {loading ? 'Signing in...' : 'Sign in '}
                </button>
            </form>
        </div>
    );
};

export default ManagerLogin;
