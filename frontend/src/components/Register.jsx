import React, { useState } from "react";

const Register = () => {
  const [role, setRole] = useState("normaluser");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cpassword, setCpassword] = useState("");
  const [phno, setPhno] = useState("");
  const [companyname, setCompanyname] = useState("");
  const [cinno, setCinno] = useState("");

const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      role,
      name,
      email,
      password,
      cpassword,
      phno,
      companyname,
      cinno,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      if (response.ok) {
        alert("✅ " + data.message);
      } else {
        alert("❌ " + data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("❌ Something went wrong!");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Enter your Name </label>
        <input
          type="text"
          required
          placeholder="Enter your name"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <br />

        <label htmlFor="email">Enter your Email </label>
        <input
          type="email"
          required
          placeholder="Enter your email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <br />

        <label htmlFor="password">Enter your Password </label>
        <input
          type="password"
          required
          placeholder="Enter password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />

        <label htmlFor="cpassword">Confirm your Password </label>
        <input
          type="password"
          required
          placeholder="Confirm password"
          id="cpassword"
          value={cpassword}
          onChange={(e) => setCpassword(e.target.value)}
        />
        <br />

        <label htmlFor="phno">Enter your Phone Number </label>
        <input
          type="text"
          required
          placeholder="Enter phone number"
          id="phno"
          value={phno}
          onChange={(e) => setPhno(e.target.value)}
        />
        <br />

        <p>Select who you are:</p>
        <input
          type="radio"
          name="role"
          id="normaluser"
          value="normaluser"
          checked={role === "normaluser"}
          onChange={(e) => setRole(e.target.value)}
        />
        <label htmlFor="normaluser">Searching for Job</label>
        <br />
        <input
          type="radio"
          name="role"
          id="recruiter"
          value="recruiter"
          checked={role === "recruiter"}
          onChange={(e) => setRole(e.target.value)}
        />
        <label htmlFor="recruiter">Recruiter</label>
        <br />

        {role === "recruiter" && (
          <div>
            <label htmlFor="companyname">Enter your Company Name </label>
            <input
              type="text"
              placeholder="Enter company name"
              required
              id="companyname"
              value={companyname}
              onChange={(e) => setCompanyname(e.target.value)}
            />
            <br />

            <label htmlFor="cinno">Enter your Company CIN Number </label>
            <input
              type="text"
              placeholder="Enter CIN number"
              required
              id="cinno"
              value={cinno}
              onChange={(e) => setCinno(e.target.value)}
            />
            <br />
          </div>
        )}

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
