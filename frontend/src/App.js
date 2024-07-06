import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from "./components/Login";
import Debug from "./components/Debug";
import StudentDashboard from "./components/StudentDashboard";
import TeacherDashboard from "./components/TeacherDashboard";
import SecretaryDashboard from './components/SecretaryDashboard';
import Register from "./components/Register";

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Debug />} /> */}
        <Route exact path="/" element={<Login />} />
        <Route exact path="/register" element={<Register />} />
        <Route path="/student-dashboard" element={<StudentDashboard />} />
        <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
        <Route path="/helpdesk-dashboard" element={<SecretaryDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
