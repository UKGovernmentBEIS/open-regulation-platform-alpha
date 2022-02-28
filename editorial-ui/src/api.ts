import axios from 'axios';

let baseURL = process.env.REACT_APP_API_BASE_URL; 

if (baseURL == undefined) { baseURL = 'http://localhost:3001'; }

const API  = axios.create({
    baseURL: baseURL
});

export default API;
