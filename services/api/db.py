"""
Database connection module with connection pooling and environment configuration.

This module provides centralized database connection management with:
- Connection pooling for efficient resource usage
- Environment variable configuration
- Error handling and connection validation
- Context manager support for safe resource cleanup
"""

import os
import logging
from contextlib import contextmanager
from typing import Generator, Optional

import psycopg2
from psycopg2 import sql, Error, OperationalError
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Configuration for database connections from environment variables."""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "analytics")
        self.user = os.getenv("DB_USER", "admin")
        self.password = os.getenv("DB_PASSWORD", "admin")
        self.min_size = int(os.getenv("DB_POOL_MIN_SIZE", "2"))
        self.max_size = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
    
    def get_connection_params(self) -> dict:
        """Return connection parameters as a dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
        }
    
    def __repr__(self) -> str:
        return (
            f"DatabaseConfig(host={self.host}, port={self.port}, "
            f"database={self.database}, user={self.user})"
        )


class ConnectionPool:
    """Manages a pool of database connections."""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._pool: Optional[SimpleConnectionPool] = None
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Initialize the connection pool."""
        try:
            params = self.config.get_connection_params()
            self._pool = SimpleConnectionPool(
                self.config.min_size,
                self.config.max_size,
                **params
            )
            logger.info(
                f"Connection pool initialized: {self.config.min_size}-"
                f"{self.config.max_size} connections to {self.config.host}:"
                f"{self.config.port}/{self.config.database}"
            )
        except Error as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise
    
    def get_connection(self) -> psycopg2.extensions.connection:
        """Get a connection from the pool."""
        if self._pool is None:
            raise RuntimeError("Connection pool not initialized")
        
        try:
            conn = self._pool.getconn()
            # Validate connection is alive
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            except (OperationalError, Error):
                # Connection is dead, close it and get a new one
                conn.close()
                conn = self._pool.getconn()
            return conn
        except Error as e:
            logger.error(f"Failed to get connection from pool: {e}")
            raise
    
    def put_connection(self, conn: psycopg2.extensions.connection) -> None:
        """Return a connection to the pool."""
        if self._pool is None:
            raise RuntimeError("Connection pool not initialized")
        
        try:
            self._pool.putconn(conn)
        except Error as e:
            logger.error(f"Failed to return connection to pool: {e}")
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        if self._pool:
            self._pool.closeall()
            logger.info("Connection pool closed")
    
    @contextmanager
    def get_db_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """Context manager for getting a database connection."""
        conn = self.get_connection()
        try:
            yield conn
        except Error as e:
            logger.error(f"Database error: {e}")
            conn.rollback()
            raise
        finally:
            self.put_connection(conn)


# Global connection pool instance
_pool: Optional[ConnectionPool] = None


def initialize_pool(config: Optional[DatabaseConfig] = None) -> ConnectionPool:
    """Initialize the global connection pool."""
    global _pool
    _pool = ConnectionPool(config)
    return _pool


def get_pool() -> ConnectionPool:
    """Get the global connection pool."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool()
    return _pool


def get_connection() -> psycopg2.extensions.connection:
    """Get a connection from the global pool."""
    return get_pool().get_connection()


@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """Context manager for getting a database connection from the global pool."""
    pool = get_pool()
    with pool.get_db_connection() as conn:
        yield conn


def close_pool() -> None:
    """Close the global connection pool."""
    global _pool
    if _pool:
        _pool.close_all()
        _pool = None
