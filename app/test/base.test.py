import pytest
from unittest.mock import patch, MagicMock
from .base import execute_query

@pytest.mark.asyncio
async def test_execute_select_query():
    # Arrange
    query = "SELECT * FROM UserVisit"
    expected_results = {
        "7938711921": {
        "ID": "7938711921",
        "FirstName": "Đức",
        "LastName": "Trung",
        "DateVisit": "2025-02-24T16:24:28",
        "LastVisit": "2025-02-24T16:24:28",
        "TotalVisit": 1,
        "IsSignin": 0,
        "DateSignin": None
        },
        "8043755190": {
        "ID": "8043755190",
        "FirstName": "aaa",
        "LastName": "bbbb",
        "DateVisit": "2025-02-24T17:29:32",
        "LastVisit": "2025-02-24T17:29:32",
        "TotalVisit": 1,
        "IsSignin": 0,
        "DateSignin": None
        }
    }
    
    # Mock the connection pool and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = expected_results
    
    with patch('mysql.connector.pooling.MySQLConnectionPool.get_connection', return_value=mock_conn):
        # Act
        results = await execute_query(query)
        
        # Assert
        assert results == expected_results
        mock_cursor.execute.assert_called_once_with(query, ())
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
