import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { AuditLog, AuditService } from '../../services/audit.service';

@Component({
  selector: 'app-audit-logs',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audit-logs.component.html',
  styleUrl: './audit-logs.component.scss'
})
export class AuditLogsComponent implements OnInit {
  logs: AuditLog[] = [];
  loading = false;
  errorMessage = '';

  constructor(
    private auditService: AuditService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.loading = true;

    this.auditService.getAuditLogs().subscribe({
      next: (response) => {
        this.logs = response.audit_logs;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Failed to load audit logs';
        this.loading = false;
      }
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}