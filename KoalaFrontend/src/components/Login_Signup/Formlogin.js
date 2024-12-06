import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import submission from "../../utils/submission";
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import LoginForm from "./LoginForm";

export default function Formlogin() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

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

    setErrors(tempErrors);

    // If there are no validation errors, proceed with the API call
    if (Object.keys(tempErrors).length === 0) {
      setLoading(true);
      try {
        const payload = {
          email: email,
          password: password,
        };

        const response = await submission("api/token/", "post", payload);

        if (response && response.access) {
          localStorage.setItem("authToken", response.access);
          setSuccessMessage("Login successful! Redirecting...");
          setTimeout(() => {
            navigate("/");
          }, 2000);
        } else {
          setErrors({ general: "Invalid email or password" });
        }
      } catch (error) {
        setErrors({ general: "An error occurred. Please try again later." });
      } finally {
        setLoading(false);
      }
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      console.log("Google credential response:", credentialResponse)
      const decoded = jwtDecode(credentialResponse.credential);
      console.log("Decoded Google token:", decoded);
      const payload = {
        email: decoded.email,
        access_token: credentialResponse.credential
      };
      
      const response = await submission("google/", "post", payload);

      if (response && response.status === "200 OK") {
        localStorage.setItem("authToken", response.access);
        setSuccessMessage("Login successful! Redirecting...");
        setTimeout(() => {
          navigate("/");
        }, 2000);
      }
    } catch (error) {
      setErrors({ general: "Google login failed. Please try again." });
    }
  };

  return (
    <GoogleOAuthProvider clientId="913758183273-5qr97tje8rcq8e2k512g2qjh25d0shre.apps.googleusercontent.com">
      <div className="flex justify-center items-center min-h-screen overflow-hidden">
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
          {/* Error Message */}
          {errors.general && (
            <div className="mt-4 text-center text-red-500">{errors.general}</div>
          )}
          {/* Success Message */}
          {successMessage && (
            <div className="mt-4 text-center text-green-500">{successMessage}</div>
          )}
          {/* Sign-up Redirect */}
          <div className="mt-8 flex justify-center items-center">
            <p className="font-medium text-base">Don't have an account?</p>
            <button
              className="ml-2 font-medium text-base text-orange-500"
              onClick={() => navigate("/signup")}
            >
              Sign up
            </button>
          </div>
          {/* Divider */}
          <div className="mt-8 flex items-center">
            <div className="flex-1 border-t border-gray-300"></div>
            <span className="px-4 text-gray-500">or</span>
            <div className="flex-1 border-t border-gray-300"></div>
          </div>
          {/* Google Login Button */}
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
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
