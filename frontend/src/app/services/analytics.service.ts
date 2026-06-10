import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface EventCount {
  total_events: number;
  error?: string;
}

export interface Product {
  product: string;
  count: number;
}

export interface Revenue {
  total_revenue: number;
  error?: string;
}

export interface ProductRevenue {
  product: string;
  revenue: number;
}

export interface EventDistribution {
  event_type: string;
  count: number;
}

@Injectable({
  providedIn: 'root',
})
export class AnalyticsService {
  private apiUrl = '/api'; // Will be proxied to backend via Docker

  constructor(private http: HttpClient) {}

  getEventCount(): Observable<EventCount> {
    return this.http.get<EventCount>(`${this.apiUrl}/events/count`);
  }

  getTopProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/analytics/top-products`);
  }

  getTotalRevenue(): Observable<Revenue> {
    return this.http.get<Revenue>(`${this.apiUrl}/analytics/revenue`);
  }

  getRevenueByProduct(): Observable<ProductRevenue[]> {
    return this.http.get<ProductRevenue[]>(
      `${this.apiUrl}/analytics/revenue-by-product`
    );
  }

  getEventDistribution(): Observable<EventDistribution[]> {
    return this.http.get<EventDistribution[]>(
      `${this.apiUrl}/analytics/event-distribution`
    );
  }
}
