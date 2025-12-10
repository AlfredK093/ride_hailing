import axios from 'axios';
const API_BASE = 'http://10.0.2.2:8000/api/v1'; // change for your environment
export default axios.create({ baseURL: API_BASE, timeout: 10000 });
