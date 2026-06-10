"""
Unit tests for FastAPI analytics endpoints.

Tests:
- Endpoint return types and structure
- Error handling
- Integration with analytics module
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from services.api.main import app

client = TestClient(app)


class TestAnalyticsEndpoints:
    """Tests for API analytics endpoints."""
    
    @patch("services.api.main.total_events")
    def test_get_event_count(self, mock_total_events):
        """Test /events/count endpoint."""
        mock_total_events.return_value = 42
        
        response = client.get("/events/count")
        assert response.status_code == 200
        assert response.json() == {"total_events": 42}
    
    @patch("services.api.main.total_events")
    def test_get_event_count_error(self, mock_total_events):
        """Test /events/count endpoint with error."""
        mock_total_events.side_effect = Exception("Database error")
        
        response = client.get("/events/count")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["total_events"] == 0
    
    @patch("services.api.main.events_by_product")
    def test_top_products(self, mock_events_by_product):
        """Test /analytics/top-products endpoint."""
        mock_events_by_product.return_value = [
            {"product": "laptop", "count": 150},
            {"product": "phone", "count": 100},
        ]
        
        response = client.get("/analytics/top-products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["product"] == "laptop"
        assert data[0]["count"] == 150
    
    @patch("services.api.main.events_by_product")
    def test_top_products_empty(self, mock_events_by_product):
        """Test /analytics/top-products with no data."""
        mock_events_by_product.return_value = []
        
        response = client.get("/analytics/top-products")
        assert response.status_code == 200
        assert response.json() == []
    
    @patch("services.api.main.events_by_product")
    def test_top_products_error(self, mock_events_by_product):
        """Test /analytics/top-products endpoint with error."""
        mock_events_by_product.side_effect = Exception("Database error")
        
        response = client.get("/analytics/top-products")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
    
    @patch("services.api.main.total_revenue")
    def test_revenue(self, mock_total_revenue):
        """Test /analytics/revenue endpoint."""
        mock_total_revenue.return_value = 5500.75
        
        response = client.get("/analytics/revenue")
        assert response.status_code == 200
        assert response.json() == {"total_revenue": 5500.75}
    
    @patch("services.api.main.total_revenue")
    def test_revenue_zero(self, mock_total_revenue):
        """Test /analytics/revenue with zero revenue."""
        mock_total_revenue.return_value = 0.0
        
        response = client.get("/analytics/revenue")
        assert response.status_code == 200
        assert response.json() == {"total_revenue": 0.0}
    
    @patch("services.api.main.total_revenue")
    def test_revenue_error(self, mock_total_revenue):
        """Test /analytics/revenue endpoint with error."""
        mock_total_revenue.side_effect = Exception("Database error")
        
        response = client.get("/analytics/revenue")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["total_revenue"] == 0
    
    @patch("services.api.main.revenue_by_product")
    def test_revenue_by_product_endpoint(self, mock_revenue_by_product):
        """Test /analytics/revenue-by-product endpoint."""
        mock_revenue_by_product.return_value = [
            {"product": "laptop", "revenue": 5000.0},
            {"product": "phone", "revenue": 3000.0},
        ]
        
        response = client.get("/analytics/revenue-by-product")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["product"] == "laptop"
        assert data[0]["revenue"] == 5000.0
    
    @patch("services.api.main.event_distribution")
    def test_event_distribution_endpoint(self, mock_event_distribution):
        """Test /analytics/event-distribution endpoint."""
        mock_event_distribution.return_value = [
            {"event_type": "view", "count": 500},
            {"event_type": "add_to_cart", "count": 150},
            {"event_type": "purchase", "count": 50},
        ]
        
        response = client.get("/analytics/event-distribution")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["event_type"] == "view"
        assert data[2]["count"] == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
