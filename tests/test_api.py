from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.schemas.producers import ProducerIntervalResponse

client = TestClient(app)

def test_get_producer_intervals_returns_404_when_empty():
    """
    Test that the /producers endpoint returns 404 when no producer intervals are found.
    """
    with patch('app.routers.producers.calculate_producer_intervals') as mock_calc:
        # Simulates empty response (without min and max)
        mock_response = MagicMock()
        mock_response.min = []
        mock_response.max = []
        mock_calc.return_value = mock_response

        response = client.get("api/v1/producers/intervals")

        assert response.status_code == 404
        assert response.json() == {"detail": "No producer intervals found."}

def test_get_producers_with_intervals_returns_200_with_valid_data():
    """
    Test that the /producers/intervals endpoint returns 200 and valid response structure
    when producer intervals are found.
    """
    with patch("app.routers.producers.calculate_producer_intervals") as mock_calc:
        mock_calc.return_value = ProducerIntervalResponse(
            min=[{"producer": "John", "interval": 1, "previousWin": 2000, "followingWin": 2001}],
            max=[{"producer": "Jane", "interval": 10, "previousWin": 1990, "followingWin": 2000}]
        )

        response = client.get("api/v1/producers/intervals")

        assert response.status_code == 200
        json_data = response.json()
        assert "min" in json_data
        assert "max" in json_data
        assert json_data["min"][0]["producer"] == "John"
        assert json_data["max"][0]["interval"] == 10

def test_get_producers_with_intervals_returns_500_on_internal_error():
    """
    Test that the /api/v1/producers/intervals endpoint returns 500 when an unexpected error occurs.
    """
    with patch("app.routers.producers.calculate_producer_intervals") as mock_calc:
        mock_calc.side_effect = Exception("Something went wrong")
        response = client.get("/api/v1/producers/intervals")
        assert response.status_code == 500

def test_get_producers_with_intervals_partial_min_only():
    """
    Test that the endpoint returns 200 even if only the min list is populated.
    """
    with patch("app.routers.producers.calculate_producer_intervals") as mock_calc:
        mock_calc.return_value = ProducerIntervalResponse(
            min=[{
                "producer": "OnlyMin",
                "interval": 2,
                "previousWin": 2001,
                "followingWin": 2003
            }],
            max=[]
        )

        response = client.get("/api/v1/producers/intervals")

        assert response.status_code == 200
        json_data = response.json()
        assert len(json_data["min"]) == 1
        assert json_data["max"] == []

def test_get_producers_with_intervals_partial_max_only():
    """
    Test that the endpoint returns 200 even if only the max list is populated.
    """
    with patch("app.routers.producers.calculate_producer_intervals") as mock_calc:
        mock_calc.return_value = ProducerIntervalResponse(
            min=[],
            max=[{
                "producer": "OnlyMax",
                "interval": 5,
                "previousWin": 1995,
                "followingWin": 2000
            }]
        )

        response = client.get("/api/v1/producers/intervals")

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["min"] == []
        assert len(json_data["max"]) == 1