import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode';
import { Container, Typography, Box, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from '@mui/material';

const SecretaryDashboard = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No token found');
                }
                const data = await api.getHelpdeskCourses();
                setCourses(data);
            } catch (error) {
                setError('Failed to fetch courses');
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);

    const handleFinalize = async (grade_id) => {
        try {
            await api.finalizeGrade(grade_id);
            setSuccess('Grade finalized successfully');
            const updatedCourses = await api.getHelpdeskCourses();
            setCourses(updatedCourses);
        } catch (error) {
            setError('Failed to finalize grade');
        } finally {
            setTimeout(() => {
                setSuccess('');
                setError('');
            }, 3000); // Clear success and error messages after 3 seconds
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
                    All Courses and Grades
                </Typography>
                {success && <Typography color="primary">{success}</Typography>}
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Course Name</TableCell>
                                <TableCell>Student Name</TableCell>
                                <TableCell>Grade</TableCell>
                                <TableCell>Finalized</TableCell>
                                <TableCell>Finalize Grade</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {courses.map((course, index) => (
                                <TableRow key={index}>
                                    <TableCell>{course.course_name}</TableCell>
                                    <TableCell>{course.student_name}</TableCell>
                                    <TableCell>{course.grade}</TableCell>
                                    <TableCell>{course.is_finalized ? 'Yes' : 'No'}</TableCell>
                                    <TableCell>
                                        <Button
                                            onClick={() => handleFinalize(course.grade_id)}
                                            disabled={course.is_finalized}
                                        >
                                            Finalize
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

export default SecretaryDashboard;
