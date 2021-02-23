import axios from 'axios'
import {API_ROOT_URL} from '../constants/utils'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const AUTHAPI = axios.create({
  baseURL: API_ROOT_URL,
  headers: {

    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})

AUTHAPI.interceptors.request.use(
  config => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config
  },
  error => {
    return Promise.reject(error.response)
  },
)

AUTHAPI.interceptors.response.use(
  response => {
    if(!response.data.error)
      return response
    else Promise.reject(response)
  },
  error => {
    if(error.response === undefined || error.response.statusText === 'Unauthorized'){
      window.location = '/login'
      return false
    }

    return Promise.reject(error.response)
  },
)

export default AUTHAPI
