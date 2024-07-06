import React, { useState } from "react";
import api from "../services/api";

const GradeForm = ({ token }) => {
    const [studentId, setStudentId] = useState("");
    const [courseId, setCourseId] = useState("");
    const [grade, setGrade] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const gradeData = {
            student_id: studentId,
            course_id: courseId,
            grade: parseFloat(grade),
        };
        await api.createGrade(token, gradeData);
        setStudentId("");
        setCourseId("");
        setGrade("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Enter Grade</h3>
            <input
                type="text"
                placeholder="Student ID"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
            />
            <input
                type="text"
                placeholder="Course ID"
                value={courseId}
                onChange={(e) => setCourseId(e.target.value)}
            />
            <input
                type="text"
                placeholder="Grade"
                value={grade}
                onChange={(e) => setGrade(e.target.value)}
            />
            <button type="submit">Submit</button>
        </form>
    );
};

export default GradeForm;
