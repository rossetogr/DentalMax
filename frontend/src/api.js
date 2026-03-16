import axios from 'axios';

// O endereço onde o seu FastAPI está rodando (Docker ou Local)
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

export default api;