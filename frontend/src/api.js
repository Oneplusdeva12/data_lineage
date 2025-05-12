import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post(`${BASE_URL}/upload`, formData);
};

export const queryLineage = (question) => {
  return axios.post(`${BASE_URL}/query`, { question });
};
