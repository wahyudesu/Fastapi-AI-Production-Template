from fastapi import APIRouter, Query, HTTPException
import httpx
from typing import Dict, Any

# Create router for MCP endpoints
router = APIRouter(prefix="/mcp", tags=["MCP Weather"])

# Predefined latitude and longitude for major cities (for simplicity)
# In a production app, you could use a geocoding service like Nominatim or Google Geocoding API
CITY_COORDINATES = {
   "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
   "San Francisco": {"lat": 37.7749, "lon": -122.4194},
   "San Diego": {"lat": 32.7157, "lon": -117.1611},
   "New York": {"lat": 40.7128, "lon": -74.0060},
   "Chicago": {"lat": 41.8781, "lon": -87.6298},
   "Miami": {"lat": 25.7617, "lon": -80.1918},
   "Seattle": {"lat": 47.6062, "lon": -122.3321},
   "Denver": {"lat": 39.7392, "lon": -104.9903},
   "Phoenix": {"lat": 33.4484, "lon": -112.0740},
   "Las Vegas": {"lat": 36.1699, "lon": -115.1398},
   # Add more cities as needed
}


@router.get("/weather")
async def get_weather(
   state_code: str = Query(..., description="State code (e.g., 'CA' for California)"),
   city: str = Query(..., description="City name (e.g., 'Los Angeles')")
) -> Dict[str, Any]:
   """
   Retrieve today's weather from the National Weather Service API based on city and state
   """
   # Get coordinates (latitude, longitude) for the given city
   if city not in CITY_COORDINATES:
       raise HTTPException(
           status_code=404,
           detail=f"City '{city}' not found in predefined list. Please use another city."
       )
  
   coordinates = CITY_COORDINATES[city]
   lat, lon = coordinates["lat"], coordinates["lon"]
    # URL for the NWS API Gridpoints endpoint
   base_url = f"https://api.weather.gov/points/{lat},{lon}"
   
   try:
       # Set up HTTP client with timeout and user agent
       headers = {
           "User-Agent": "FastAPI-MCP-Weather/1.0 (Contact: admin@yourapp.com)"
       }
       
       async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
           # First, get the gridpoint information for the given location
           gridpoint_response = await client.get(base_url)
           gridpoint_response.raise_for_status()
           gridpoint_data = gridpoint_response.json()
          
           # Retrieve the forecast data using the gridpoint information
           forecast_url = gridpoint_data["properties"]["forecast"]
           forecast_response = await client.get(forecast_url)
           forecast_response.raise_for_status()
           forecast_data = forecast_response.json()


           # Returning today's forecast
           today_weather = forecast_data["properties"]["periods"][0]
           return {
               "city": city,
               "state": state_code,
               "coordinates": {"lat": lat, "lon": lon},
               "date": today_weather["startTime"],
               "temperature": today_weather["temperature"],
               "temperatureUnit": today_weather["temperatureUnit"],
               "forecast": today_weather["detailedForecast"],
               "windSpeed": today_weather.get("windSpeed", "N/A"),
               "windDirection": today_weather.get("windDirection", "N/A"),
           }
  
   except httpx.HTTPStatusError as e:
       raise HTTPException(
           status_code=e.response.status_code,
           detail=f"NWS API error: {e.response.text}"
       )
   except Exception as e:
       raise HTTPException(
           status_code=500,
           detail=f"Internal server error: {str(e)}"
       )


@router.get("/cities")
async def get_available_cities() -> Dict[str, Any]:
    """
    Get list of available cities for weather lookup
    """
    return {
        "available_cities": list(CITY_COORDINATES.keys()),
        "total_cities": len(CITY_COORDINATES),
        "usage": "Use these city names with the /weather endpoint"
    }