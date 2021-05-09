import axios from 'axios'
export const API_BASE_URL = '//localhost:8000/'

export const http = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
    // Authorization: 'Bearer ' + localStorage.getItem('user-token')
  }
})

export default http
