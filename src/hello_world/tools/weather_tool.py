from crewai.tools import BaseTool
import requests
from typing import Optional, Dict, Any, Type
from pydantic import BaseModel, Field


class CustomApiToolInputSchema(BaseModel):
    # endpoint: str = Field(..., description="The specific endpoint for the API call")
    # method: str = Field(..., description="HTTP method to use (GET, POST, PUT, DELETE)")
    # headers: Optional[Dict[str, str]] = Field(None, description="HTTP headers to include in the request")
    # query_params: Optional[Dict[str, Any]] = Field(None, description="Query parameters for the request")
    # body: Optional[Dict[str, Any]] = Field(None, description="Body of the request for POST/PUT methods")
    city: str = Field(..., description="The city for the Weather Report")


class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Gets the weather for a specific city"
    args_schema: Type[BaseModel] = CustomApiToolInputSchema

    def _run(self, city: str) -> str:
        api_key = "bf9012ad8b704c1784f175544252404"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            return f"The current temperature in {city} is {temp}°C with {condition}."
        else:
            return f"Failed to get weather data for {city}."
