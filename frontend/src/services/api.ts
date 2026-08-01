import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  // FastAPI reads repeated list parameters as ?tags=a&tags=b. Axios would
  // otherwise bracket them as tags[]=a, which the backend does not match.
  paramsSerializer: {
    indexes: null
  }
})

export default api
