import axios from 'axios';

const API_URL = 'http://localhost:8000';

const getToken = () => localStorage.getItem('token');

const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/token`, new URLSearchParams({
        username: username,
        password: password,
    }), {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    return response.data;
};

const getStudentCourses = async (user_id) => {
    const token = getToken();
    const response = await axios.get(`${API_URL}/students/${user_id}/courses`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

const getTeacherCourses = async (teacher_id) => {
    const token = getToken();
    const response = await axios.get(`${API_URL}/teachers/${teacher_id}/courses`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

const updateGrade = async (grade_id, grade) => {
    const token = getToken();
    const response = await axios.put(`${API_URL}/grades/${grade_id}`, { grade }, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

const getHelpdeskCourses = async () => {
    const token = getToken();
    const response = await axios.get(`${API_URL}/helpdesk/courses`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

const finalizeGrade = async (grade_id) => {
    const token = getToken();
    const response = await axios.put(`${API_URL}/grades/${grade_id}/finalize`, {}, {
        headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};

const api = {
    login,
    getStudentCourses,
    getTeacherCourses,
    updateGrade,
    getHelpdeskCourses,
    finalizeGrade
};

export default api;
