export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  username: string;
  role: string; 
}

export interface DeviceResponse {
  id: number;
  serial_number: string;
  location: string | null;
  is_active: boolean;
}

export interface WasteTypeResponse {
  id: number;
  name: string; 
}

export interface ContainerResponse {
  id: number;
  device_id: number;
  waste_type_id: number;
  fill_level: number;
}

export interface SensorDataResponse {
  id: number;
  container_id: number;
  fill_level: number;
  created_at: string;
}

export interface RouteResponse {
  id: number;
  description: string | null;
  created_at: string;
}

export interface AlertResponse {
  id: number;
  container_id: number;
  message: string;
  created_at: string;
}