import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { Device, DeviceService } from '../../services/device.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  devices: Device[] = [];
  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private deviceService: DeviceService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadDevices();
  }

  loadDevices(): void {
    this.loading = true;
    this.errorMessage = '';

    this.deviceService.getDevices().subscribe({
      next: (response) => {
        this.devices = response.devices;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Failed to load devices';
        this.loading = false;
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  scrollToSection(sectionId: string): void {
    const section = document.getElementById(sectionId);
    section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  goToDashboard(): void {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  goToDevices(): void {
    this.scrollToSection('devices-section');
  }

  goToFirmware(): void {
    this.scrollToSection('firmware-section');
  }

  goToHealth(): void {
    this.scrollToSection('health-section');
  }

  goToAuditLogs(): void {
    this.router.navigate(['/audit-logs']);
  }

  goToReports(): void {
    window.open('/reports/full_test_report.html', '_blank');
  }

  updatePower(device: Device, power: string): void {
    this.clearMessages();

    this.deviceService.updatePower(device.id, power).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        this.loadDevices();
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Power update failed';
      }
    });
  }

  updateTemperature(device: Device, input: HTMLInputElement): void {
    this.clearMessages();
    const value = Number(input.value);

    this.deviceService.updateTemperature(device.id, value).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        input.value = '';
        this.loadDevices();
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Temperature update failed';
      }
    });
  }

  updateVolume(device: Device, input: HTMLInputElement): void {
    this.clearMessages();
    const value = Number(input.value);

    this.deviceService.updateVolume(device.id, value).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        input.value = '';
        this.loadDevices();
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Volume update failed';
      }
    });
  }

  updateWasher(device: Device, waterInput: HTMLInputElement): void {
    this.clearMessages();
    const waterLevel = Number(waterInput.value || 3);

    this.deviceService.updateCycle(device.id, 'START', waterLevel).subscribe({
      next: (response) => {
        this.successMessage = response.message;
        waterInput.value = '';
        this.loadDevices();
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Cycle update failed';
      }
    });
  }

  clearMessages(): void {
    this.successMessage = '';
    this.errorMessage = '';
  }

  get totalDevices(): number {
    return this.devices.length;
  }

  get onlineDevices(): number {
    return this.devices.filter(device => device.status === 'ONLINE').length;
  }

  get poweredOnDevices(): number {
    return this.devices.filter(device => device.power === 'ON').length;
  }

  get healthyDevices(): number {
    return this.devices.filter(device => device.health_status === 'HEALTHY').length;
  }

  get firmwareUpdatedDevices(): number {
    return this.devices.filter(device => !!device.firmware_version).length;
  }
}