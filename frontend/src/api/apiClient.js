import axios from 'axios';

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

function afterLogoutCleanup() {
  sessionStorage.removeItem('dashboardUsername');
}

/**
 * End session on the server (httpOnly cookies) and clear non-sensitive client state.
 */
export function clearAuth() {
  return api
    .post('/auth/logout/')
    .catch(() => {})
    .then(() => {
      afterLogoutCleanup();
    });
}

let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (!original || error.response?.status !== 401) {
      return Promise.reject(error);
    }
    const url = original.url || '';
    if (url.includes('auth/ping')) {
      return Promise.reject(error);
    }
    if (url.includes('token/refresh')) {
      return Promise.reject(error);
    }
    if (url.includes('token') && original.method === 'post') {
      return Promise.reject(error);
    }
    if (original._retry) {
      return Promise.reject(error);
    }
    original._retry = true;
    try {
      if (!refreshPromise) {
        refreshPromise = api
          .post('/token/refresh/', {})
          .then((res) => {
            refreshPromise = null;
            return res;
          })
          .catch((err) => {
            refreshPromise = null;
            throw err;
          });
      }
      await refreshPromise;
      return api(original);
    } catch {
      await api.post('/auth/logout/').catch(() => {});
      afterLogoutCleanup();
      window.location.reload();
      return Promise.reject(error);
    }
  }
);

export default api;
