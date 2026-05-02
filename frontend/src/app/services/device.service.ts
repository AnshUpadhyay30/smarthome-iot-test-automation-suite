import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Device {
  id: number;
  name: string;
  type: string;
  status: string;
  power: string;
  temperature: number | null;
  freezer_temperature: number | null;
  volume: number | null;
  mode: string | null;
  cycle_status: string | null;
  water_level: number | null;
  firmware_version: string;
  health_status: string | null;
  error_code: string | null;
  wifi_signal: string | null;
  owner_id: number;
}

interface DevicesResponse {
  devices: Device[];
}

interface DeviceUpdateResponse {
  message: string;
  device: Device;
}

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  private readonly apiUrl = 'http://127.0.0.1:5000/api/devices';

  constructor(private http: HttpClient) {}

  getDevices(): Observable<DevicesResponse> {
    return this.http.get<DevicesResponse>(this.apiUrl);
  }

  updatePower(deviceId: number, power: string): Observable<DeviceUpdateResponse> {
    return this.http.patch<DeviceUpdateResponse>(`${this.apiUrl}/${deviceId}/power`, {
      power
    });
  }

  updateTemperature(deviceId: number, temperature: number): Observable<DeviceUpdateResponse> {
    return this.http.patch<DeviceUpdateResponse>(`${this.apiUrl}/${deviceId}/temperature`, {
      temperature
    });
  }

  updateVolume(deviceId: number, volume: number): Observable<DeviceUpdateResponse> {
    return this.http.patch<DeviceUpdateResponse>(`${this.apiUrl}/${deviceId}/volume`, {
      volume
    });
  }

  updateCycle(deviceId: number, cycleStatus: string, waterLevel: number): Observable<DeviceUpdateResponse> {
    return this.http.patch<DeviceUpdateResponse>(`${this.apiUrl}/${deviceId}/cycle`, {
      cycle_status: cycleStatus,
      water_level: waterLevel
    });
  }
}