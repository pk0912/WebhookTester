import axios from 'axios'
// export const API_BASE_URL = 'http://ec2-3-108-26-46.ap-south-1.compute.amazonaws.com/api'
export const API_BASE_URL = '//localhost:8000/api/'

export const http = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
    // Authorization: 'Bearer ' + localStorage.getItem('user-token')
  }
})

export default http
