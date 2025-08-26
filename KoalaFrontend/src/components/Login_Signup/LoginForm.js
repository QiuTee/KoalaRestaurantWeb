import React from "react";
import SigninButton from "../Button/SigninButton";

export default function LoginForm({ email, setEmail, password, setPassword, errors, handleSubmit, loading }) {
  return (
    <div className="mt-8">
      {/* Email Field */}
      <div className="flex flex-col">
        <label className="text-lg font-medium">Email</label>
        <input
          className={`w-full border-2 ${errors.email ? "border-red-500" : "border-gray-100"} rounded-xl p-4 mt-1 bg-transparent`}
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {errors.email && <span className="text-red-500 mt-1">{errors.email}</span>}
      </div>

      {/* Password Field */}
      <div className="flex flex-col mt-4">
        <label className="text-lg font-medium">Password</label>
        <input
          className={`w-full border-2 ${errors.password ? "border-red-500" : "border-gray-100"} rounded-xl p-4 mt-1 bg-transparent`}
          placeholder="Enter your password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {errors.password && <span className="text-red-500 mt-1">{errors.password}</span>}
      </div>

      {/* Sign in Button */}
      <div className="mt-8 flex flex-col gap-y-4 items-center">
        <span className="whitespace-nowrap">
          <button onClick={handleSubmit} disabled={loading}>
            <SigninButton />
          </button>
        </span>
      </div>
    </div>
  );
} 