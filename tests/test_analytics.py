"""
Unit tests for analytics queries module.

Tests:
- Query function return types and structure
- Error handling
- Mock database responses
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from services.analytics.queries import (
    total_events,
    total_revenue,
    events_by_product,
    revenue_by_product,
    event_distribution,
)


class TestAnalyticsQueries:
    """Tests for analytics query functions."""
    
    @patch("services.analytics.queries.get_conn")
    def test_total_events(self, mock_get_conn):
        """Test total_events returns integer count."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (42,)
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = total_events()
        assert result == 42
        assert isinstance(result, int)
    
    @patch("services.analytics.queries.get_conn")
    def test_total_revenue(self, mock_get_conn):
        """Test total_revenue returns float."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1500.50,)
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = total_revenue()
        assert result == 1500.50
        assert isinstance(result, float)
    
    @patch("services.analytics.queries.get_conn")
    def test_total_revenue_null_handling(self, mock_get_conn):
        """Test total_revenue handles NULL from database."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (None,)
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = total_revenue()
        assert result == 0.0
    
    @patch("services.analytics.queries.get_conn")
    def test_events_by_product(self, mock_get_conn):
        """Test events_by_product returns list of dicts."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("laptop", 150),
            ("phone", 100),
            ("keyboard", 50),
        ]
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = events_by_product()
        assert len(result) == 3
        assert result[0] == {"product": "laptop", "count": 150}
        assert result[1] == {"product": "phone", "count": 100}
    
    @patch("services.analytics.queries.get_conn")
    def test_events_by_product_empty(self, mock_get_conn):
        """Test events_by_product with empty database."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = events_by_product()
        assert result == []
    
    @patch("services.analytics.queries.get_conn")
    def test_revenue_by_product(self, mock_get_conn):
        """Test revenue_by_product returns list of dicts with float revenue."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("laptop", 5000.00),
            ("phone", 3000.00),
        ]
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = revenue_by_product()
        assert len(result) == 2
        assert result[0]["product"] == "laptop"
        assert result[0]["revenue"] == 5000.0
        assert isinstance(result[0]["revenue"], float)
    
    @patch("services.analytics.queries.get_conn")
    def test_revenue_by_product_null_handling(self, mock_get_conn):
        """Test revenue_by_product handles NULL revenue."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("laptop", None),
        ]
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = revenue_by_product()
        assert result[0]["revenue"] == 0.0
    
    @patch("services.analytics.queries.get_conn")
    def test_event_distribution(self, mock_get_conn):
        """Test event_distribution returns list of event types and counts."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("view", 500),
            ("add_to_cart", 150),
            ("purchase", 50),
        ]
        
        mock_cursor.__enter__ = Mock(return_value=mock_cursor)
        mock_cursor.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor
        
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=False)
        mock_get_conn.return_value = mock_conn
        
        result = event_distribution()
        assert len(result) == 3
        assert result[0] == {"event_type": "view", "count": 500}
        assert result[1]["event_type"] == "add_to_cart"
        assert result[2]["count"] == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
