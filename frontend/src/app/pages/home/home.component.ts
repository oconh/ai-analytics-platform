import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsService } from '../../services/analytics.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  eventCount: number = 0;
  totalRevenue: number = 0;
  topProducts: any[] = [];
  eventDistribution: any[] = [];
  loading = true;
  error: string | null = null;

  constructor(private analyticsService: AnalyticsService) {}

  ngOnInit() {
    this.loadDashboard();
  }

  loadDashboard() {
    this.loading = true;
    this.error = null;

    // Load event count
    this.analyticsService.getEventCount().subscribe({
      next: (data) => {
        this.eventCount = data.total_events;
      },
      error: (err) => {
        console.error('Error loading event count:', err);
        this.error = 'Failed to load event count';
      },
    });

    // Load total revenue
    this.analyticsService.getTotalRevenue().subscribe({
      next: (data) => {
        this.totalRevenue = data.total_revenue;
      },
      error: (err) => {
        console.error('Error loading revenue:', err);
      },
    });

    // Load top products
    this.analyticsService.getTopProducts().subscribe({
      next: (data) => {
        this.topProducts = data.slice(0, 5); // Top 5
      },
      error: (err) => {
        console.error('Error loading products:', err);
      },
    });

    // Load event distribution
    this.analyticsService.getEventDistribution().subscribe({
      next: (data) => {
        this.eventDistribution = data;
      },
      error: (err) => {
        console.error('Error loading distribution:', err);
      },
      complete: () => {
        this.loading = false;
      },
    });
  }
}
