import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AuditLog {
  id: number;
  device_id: number;
  device_name: string;
  action: string;
  old_value: string | null;
  new_value: string | null;
  message: string;
  created_at: string;
}

interface AuditLogsResponse {
  audit_logs: AuditLog[];
}

@Injectable({
  providedIn: 'root'
})
export class AuditService {
  private readonly apiUrl = 'http://127.0.0.1:5000/api/audit-logs';

  constructor(private http: HttpClient) {}

  getAuditLogs(): Observable<AuditLogsResponse> {
    return this.http.get<AuditLogsResponse>(this.apiUrl);
  }
}