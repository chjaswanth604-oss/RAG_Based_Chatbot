import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor to handle 401 unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth Services
export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Chat Services
export const chatService = {
  sendMessage: (data) => api.post('/chat', data),
  getHistory: () => api.get('/chat/history'),
  getChatDetail: (chatId) => api.get(`/chat/${chatId}`),
  deleteChat: (chatId) => api.delete(`/chat/${chatId}`),
};

// Document Services
export const documentService = {
  uploadDocument: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getDocuments: () => api.get('/documents'),
  deleteDocument: (id) => api.delete(`/documents/${id}`),
  replaceDocument: (id, formData) => api.put(`/documents/${id}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

// Feedback Service
export const feedbackService = {
  submitFeedback: (data) => api.post('/feedback', data),
};

// Admin Service
export const adminService = {
  getStats: () => api.get('/admin/stats'),
};

export default api;
