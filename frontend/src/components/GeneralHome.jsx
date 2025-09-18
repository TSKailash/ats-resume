import React from "react";
import Navbar from "./Navbar";
import { useNavigate } from "react-router-dom";

const GeneralHome = () => {

    const navigate = useNavigate();

    const handleLoginBtn =()=>{
        navigate("/login");
    }

    const handleRegisterBtn =()=>{
        navigate("/register");
    }
  return (
    
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center flex-grow px-6 text-center">
        <h1 className="text-5xl font-extrabold text-gray-900 leading-tight drop-shadow-sm">
          ATS Resume Analyser <br /> & Recruiter Tool
        </h1>
        <p className="mt-4 text-lg text-gray-600 max-w-2xl">
          Empower your hiring process with AI-driven resume analysis and an
          intuitive recruitment dashboard.
        </p>

        {/* Action Buttons */}
        <div className="mt-8 flex gap-6">
          <button className="px-8 py-3 rounded-full bg-blue-600 text-white text-lg font-medium shadow-lg hover:bg-blue-700 hover:scale-105 transition" onClick={handleLoginBtn}>
            Login
          </button>
          <button className="px-8 py-3 rounded-full bg-green-500 text-white text-lg font-medium shadow-lg hover:bg-green-600 hover:scale-105 transition" onClick={handleRegisterBtn}>
            Register
          </button>
        </div>
      </div>

      {/* Footer Section */}
      <footer className="py-6 text-center text-gray-500 text-sm">
        © {new Date().getFullYear()} ATS Resume Analyser. All rights reserved.
      </footer>
    </div>
  );
};

export default GeneralHome;
