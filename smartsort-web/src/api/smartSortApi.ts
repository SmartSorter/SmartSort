import axiosClient from './axiosClient';
import type {
    TokenResponse,
    ContainerResponse,
    AlertResponse,
    RouteResponse,
    DeviceResponse,
    WasteTypeResponse
} from '../types/api';

export const smartSortApi = {
  login: async (username: string, password: string): Promise<TokenResponse> => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await axiosClient.post('/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
async register(username: string, password: string, role: string): Promise<any> {
  const response = await axiosClient.post('/users/', {
    username,
    password,
    role
  });
  return response.data;
},
  getContainers: async (): Promise<ContainerResponse[]> => {
    const response = await axiosClient.get('/containers/');
    return response.data;
  },

  getAlerts: async (): Promise<AlertResponse[]> => {
    const response = await axiosClient.get('/alerts/');
    return response.data;
  },

  optimizeRoutes: async (): Promise<RouteResponse> => {
    const response = await axiosClient.post('/routes/optimize');
    return response.data;
  },

  getDevices: async (): Promise<DeviceResponse[]> => {
    const response = await axiosClient.get('/devices/');
    return response.data;
  },

  getWasteTypes: async (): Promise<WasteTypeResponse[]> => {
    const response = await axiosClient.get('/waste-types/');
    return response.data;
  }
};