import axios from 'axios'
import {API_ROOT_URL} from '../constants/utils'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const API = axios.create({
  baseURL: API_ROOT_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

API.interceptors.response.use(
  response => {
    return response
  },
  error => {
    return Promise.reject(error.response)
  },
)

export default API
