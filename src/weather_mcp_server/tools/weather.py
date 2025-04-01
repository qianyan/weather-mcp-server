import logging
import os
from typing import Dict, Optional

import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    """天气查询响应模型"""

    temperature: float = Field(..., description="温度")
    humidity: float = Field(..., description="湿度")
    description: str = Field(..., description="天气描述")
    city: str = Field(..., description="城市名称")


class WeatherTools:
    """天气查询工具集"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 OPENWEATHER_API_KEY 环境变量")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def register_tools(self, mcp: FastMCP):
        """注册 MCP 工具"""

        @mcp.tool("获取指定城市的天气信息")
        def get_weather(city: str, units: Optional[str] = "metric") -> Dict:
            """
            获取指定城市的天气信息

            Args:
                city: 城市名称
                units: 温度单位 (metric: 摄氏度, imperial: 华氏度)
            """
            try:
                self.logger.info(f"获取城市 {city} 的天气信息")
                params = {"q": city, "appid": self.api_key, "units": units}

                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                result = WeatherResponse(
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    description=data["weather"][0]["description"],
                    city=data["name"],
                )

                return result.model_dump()
            except Exception as e:
                self.logger.error(f"获取天气信息失败: {str(e)}")
                raise
