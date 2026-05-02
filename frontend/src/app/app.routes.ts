import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { AuditLogsComponent } from './pages/audit-logs/audit-logs.component';
import { DeviceDetailComponent } from './pages/device-detail/device-detail.component';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard]
  },
  {
    path: 'audit-logs',
    component: AuditLogsComponent,
    canActivate: [authGuard]
  },
  {
    path: 'devices/:id',
    component: DeviceDetailComponent,
    canActivate: [authGuard]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];