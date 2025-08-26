import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import submission from "../../utils/submission";
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import LoginForm from "./LoginForm";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ReCAPTCHA from "react-google-recaptcha"; // Import thư viện reCAPTCHA

export default function Formlogin() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [recaptchaToken, setRecaptchaToken] = useState(""); 
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [showRecaptcha, setShowRecaptcha] = useState(false); 

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      localStorage.removeItem("authToken");
    }
  }, []);

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleSubmit = async () => {
    let tempErrors = {};

    // Basic validations for email and password
    if (!email) {
      tempErrors.email = "Email is required";
    } else if (!validateEmail(email)) {
      tempErrors.email = "Email is not valid";
    }

    if (!password) {
      tempErrors.password = "Password is required";
    }

    if (!recaptchaToken && showRecaptcha) {
      tempErrors.recaptcha = "Please verify that you are not a robot";
    }

    setErrors(tempErrors);

    // If there are no validation errors, proceed with the API call
    if (Object.keys(tempErrors).length === 0) {
      setLoading(true);
      try {
        const payload = {
          email: email,
          password: password,
          recaptcha: recaptchaToken || null, // Gửi token reCAPTCHA nếu có
        };

        const response = await submission("authentication/customer/login/", "post", payload);

        if (response && response.status === "200") {
          localStorage.setItem("authToken", response.data.access);
          toast.success(response.message);
          setTimeout(() => {
            navigate("/");
          }, 2000);
        } else {
          toast.error("Email or password is incorrect");
        }
      } catch (error) {
        if (error.response?.status === 429) {
          toast.error("Too many login attempts. Please complete the reCAPTCHA.");
          setShowRecaptcha(true);
        } else {
          toast.error("An error occurred. Please try again later.");
        }
      } finally {
        setLoading(false);
      }
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      console.log("Google credential response:", credentialResponse);
      const decoded = jwtDecode(credentialResponse.credential);
      console.log("Decoded Google token:", decoded);
      const payload = {
        email: decoded.email,
        access_token: credentialResponse.credential,
      };
      
      const response = await submission("authentication/google/", "post", payload);

      if (response && response.status === "200 OK") {
        localStorage.setItem("authToken", response.access);
        toast.success("Google login successful!");
        setSuccessMessage("Login successful! Redirecting...");
        setTimeout(() => {
          navigate("/");
        }, 2000);
      } else {
        toast.error("Google login failed. Please try again.");
        setErrors({ general: "Google login failed. Please try again." });
      }
    } catch (error) {
      toast.error("Google login failed. Please try again.");
      setErrors({ general: "Google login failed. Please try again." });
    }
  };

  const handleRecaptchaChange = (token) => {
    setRecaptchaToken(token); // Lưu token khi reCAPTCHA được xác minh
  };

  return (
    <GoogleOAuthProvider clientId="913758183273-5qr97tje8rcq8e2k512g2qjh25d0shre.apps.googleusercontent.com">
      <div className="flex justify-center items-center min-h-screen overflow-hidden">
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
        <div className="w-11/12 max-w-[700px] px-10 py-20 rounded-3xl bg-white border-2 border-gray-100">
          <h1 className="text-5xl font-semibold">Welcome to our restaurant</h1>
          <p className="font-medium text-lg text-gray-500 mt-4">
            Welcome! Please enter your details.
          </p>
          <LoginForm
            email={email}
            setEmail={setEmail}
            password={password}
            setPassword={setPassword}
            errors={errors}
            handleSubmit={handleSubmit}
            loading={loading}
          />
          {errors.general && (
            <div className="mt-4 text-center text-red-500">{errors.general}</div>
          )}
          {successMessage && (
            <div className="mt-4 text-center text-green-500">{successMessage}</div>
          )}
          <div className="mt-8 flex justify-center items-center">
            <p className="font-medium text-base">Don't have an account?</p>
            <button
              className="ml-2 font-medium text-base text-orange-500"
              onClick={() => navigate("/signup")}
            >
              Sign up
            </button>
          </div>
          <div className="mt-8 flex items-center">
            <div className="flex-1 border-t border-gray-300"></div>
            <span className="px-4 text-gray-500">or</span>
            <div className="flex-1 border-t border-gray-300"></div>
          </div>
          <div className="mt-8">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                setErrors({ general: "Google login failed" });
              }}
              theme="outline"
              size="large"
              width="100%"
              text="signin_with"
              shape="rectangular"
              locale="en"
            />
          </div>
          {showRecaptcha && (
            <div className="mt-4">
              <ReCAPTCHA
                sitekey="6LeZM5UqAAAAAMxEapzr-UbNvcupx_wV6vWf_zdI" 
                onChange={handleRecaptchaChange}
              />
              {errors.recaptcha && (
                <div className="mt-2 text-red-500 text-sm">{errors.recaptcha}</div>
              )}
            </div>
          )}
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}

