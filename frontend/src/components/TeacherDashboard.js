import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode';
import { Container, Typography, Box, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, TextField } from '@mui/material';

const TeacherDashboard = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [grades, setGrades] = useState({});

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No token found');
                }
                const decodedToken = jwtDecode(token);
                const teacher_id = decodedToken.sub;  // Now sub should be user_id
                const data = await api.getTeacherCourses(teacher_id);
                setCourses(data);
            } catch (error) {
                setError('Failed to fetch courses');
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);


    const handleGradeChange = (grade_id, value) => {
        setGrades((prevGrades) => ({
            ...prevGrades,
            [grade_id]: value,
        }));
    };

    const handleGradeUpdate = async (grade_id) => {
        if (grades[grade_id] !== undefined) {
            try {
                await api.updateGrade(grade_id, parseFloat(grades[grade_id]));
                const token = localStorage.getItem('token');
                const decodedToken = jwtDecode(token);
                const teacher_id = decodedToken.sub;
                const updatedCourses = await api.getTeacherCourses(teacher_id);
                setCourses(updatedCourses);
                setGrades((prevGrades) => ({
                    ...prevGrades,
                    [grade_id]: '',
                }));
            } catch (error) {
                setError('Failed to update grade');
            }
        }
    };

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">{error}</Typography>;
    }

    return (
        <Container>
            <Box sx={{ mt: 4 }}>
                <Typography variant="h4" gutterBottom>
                    My Courses and Students
                </Typography>
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Course Name</TableCell>
                                <TableCell>Student Name</TableCell>
                                <TableCell>Grade</TableCell>
                                <TableCell>Update Grade</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {courses.map((course, index) => (
                                <TableRow key={index}>
                                    <TableCell>{course.course_name}</TableCell>
                                    <TableCell>{course.student_name}</TableCell>
                                    <TableCell>{course.grade}</TableCell>
                                    <TableCell>
                                        <TextField
                                            size="small"
                                            type="number"
                                            value={grades[course.grade_id] || ''}
                                            onChange={(e) => handleGradeChange(course.grade_id, e.target.value)}
                                        />
                                        <Button onClick={() => handleGradeUpdate(course.grade_id)} disabled={!grades[course.grade_id]}>
                                            Update
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>
        </Container>
    );
};


export default TeacherDashboard;
