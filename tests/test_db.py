"""
Unit tests for database connection module.

Tests:
- DatabaseConfig initialization and parameter retrieval
- ConnectionPool initialization
- Connection acquisition and release
- Connection validation
- Context manager behavior
- Error handling
- Pool cleanup
"""

import os
import pytest
import logging
from unittest.mock import Mock, patch, MagicMock

from services.api.db import (
    DatabaseConfig,
    ConnectionPool,
    get_pool,
    get_connection,
    get_db_connection,
    initialize_pool,
    close_pool,
)


class TestDatabaseConfig:
    """Tests for DatabaseConfig class."""
    
    def test_config_from_env_vars(self):
        """Test that DatabaseConfig reads environment variables."""
        with patch.dict(os.environ, {
            "DB_HOST": "testhost",
            "DB_PORT": "5433",
            "DB_NAME": "testdb",
            "DB_USER": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_POOL_MIN_SIZE": "5",
            "DB_POOL_MAX_SIZE": "20",
        }):
            config = DatabaseConfig()
            
            assert config.host == "testhost"
            assert config.port == 5433
            assert config.database == "testdb"
            assert config.user == "testuser"
            assert config.password == "testpass"
            assert config.min_size == 5
            assert config.max_size == 20
    
    def test_config_defaults(self):
        """Test that DatabaseConfig uses default values when env vars not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = DatabaseConfig()
            
            assert config.host == "localhost"
            assert config.port == 5432
            assert config.database == "analytics"
            assert config.user == "admin"
            assert config.password == "admin"
            assert config.min_size == 2
            assert config.max_size == 10
    
    def test_get_connection_params(self):
        """Test that get_connection_params returns correct dictionary."""
        with patch.dict(os.environ, {
            "DB_HOST": "myhost",
            "DB_USER": "myuser",
            "DB_PASSWORD": "mypass",
        }):
            config = DatabaseConfig()
            params = config.get_connection_params()
            
            assert params["host"] == "myhost"
            assert params["user"] == "myuser"
            assert params["password"] == "mypass"
            assert "database" in params
            assert "port" in params
    
    def test_config_repr(self):
        """Test string representation of DatabaseConfig."""
        config = DatabaseConfig()
        repr_str = repr(config)
        
        assert "DatabaseConfig" in repr_str
        assert "localhost" in repr_str
        assert "5432" in repr_str


class TestConnectionPool:
    """Tests for ConnectionPool class."""
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_initialization(self, mock_pool_class):
        """Test that ConnectionPool initializes correctly."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        
        config = DatabaseConfig()
        pool = ConnectionPool(config)
        
        assert pool._pool is not None
        mock_pool_class.assert_called_once()
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_get_connection(self, mock_pool_class):
        """Test getting a connection from the pool."""
        mock_pool_instance = Mock()
        mock_connection = Mock()
        mock_connection.cursor = MagicMock()
        mock_pool_instance.getconn.return_value = mock_connection
        mock_pool_class.return_value = mock_pool_instance
        
        config = DatabaseConfig()
        pool = ConnectionPool(config)
        conn = pool.get_connection()
        
        assert conn is not None
        mock_pool_instance.getconn.assert_called_once()
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_put_connection(self, mock_pool_class):
        """Test returning a connection to the pool."""
        mock_pool_instance = Mock()
        mock_connection = Mock()
        mock_pool_class.return_value = mock_pool_instance
        
        config = DatabaseConfig()
        pool = ConnectionPool(config)
        pool.put_connection(mock_connection)
        
        mock_pool_instance.putconn.assert_called_once_with(mock_connection)
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_close_all(self, mock_pool_class):
        """Test closing all connections in the pool."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        
        config = DatabaseConfig()
        pool = ConnectionPool(config)
        pool.close_all()
        
        mock_pool_instance.closeall.assert_called_once()
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_context_manager(self, mock_pool_class):
        """Test using pool as a context manager."""
        mock_pool_instance = Mock()
        mock_connection = Mock()
        mock_cursor = Mock()
        
        # Setup cursor context manager
        mock_connection.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_connection.cursor.return_value.__exit__ = Mock(return_value=False)
        mock_cursor.execute = Mock()
        
        mock_pool_instance.getconn.return_value = mock_connection
        mock_pool_class.return_value = mock_pool_instance
        
        config = DatabaseConfig()
        pool = ConnectionPool(config)
        
        with pool.get_db_connection() as conn:
            assert conn is mock_connection
        
        # Verify connection was returned to pool
        mock_pool_instance.putconn.assert_called_once_with(mock_connection)


class TestGlobalPoolFunctions:
    """Tests for global pool management functions."""
    
    @patch("services.api.db.ConnectionPool")
    def test_initialize_pool(self, mock_pool_class):
        """Test initializing the global pool."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        
        # Clear any existing pool
        import services.api.db as db_module
        db_module._pool = None
        
        result = initialize_pool()
        assert result is not None
    
    @patch("services.api.db.ConnectionPool")
    def test_get_pool(self, mock_pool_class):
        """Test getting the global pool."""
        mock_pool_instance = Mock()
        mock_pool_class.return_value = mock_pool_instance
        
        # Clear any existing pool
        import services.api.db as db_module
        db_module._pool = None
        
        pool = get_pool()
        assert pool is not None


class TestConnectionIntegration:
    """Integration-level tests for database connections."""
    
    def test_get_db_connection_context_manager_signature(self):
        """Test that get_db_connection returns a context manager."""
        with patch("services.api.db.get_pool") as mock_get_pool:
            mock_pool = Mock()
            mock_connection = Mock()
            mock_pool.get_db_connection.return_value.__enter__ = Mock(
                return_value=mock_connection
            )
            mock_pool.get_db_connection.return_value.__exit__ = Mock(
                return_value=False
            )
            mock_get_pool.return_value = mock_pool
            
            with get_db_connection() as conn:
                assert conn is mock_connection


class TestErrorHandling:
    """Tests for error handling in database module."""
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_pool_initialization_error(self, mock_pool_class):
        """Test that pool initialization errors are raised."""
        from psycopg2 import Error
        mock_pool_class.side_effect = Error("Connection failed")
        
        with pytest.raises(Error):
            ConnectionPool()
    
    @patch("services.api.db.SimpleConnectionPool")
    def test_get_connection_when_pool_not_initialized(self, mock_pool_class):
        """Test error when trying to get connection from uninitialized pool."""
        mock_pool_instance = Mock()
        mock_pool_instance.getconn.side_effect = Exception("Pool error")
        mock_pool_class.return_value = mock_pool_instance
        
        pool = ConnectionPool()
        with pytest.raises(Exception):
            pool.get_connection()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
