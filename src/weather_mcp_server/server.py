import logging

from dotenv import load_dotenv
from fastmcp import FastMCP

from .tools.weather import WeatherTools

# 加载 .env 文件中的环境变量
load_dotenv()


class WeatherMCPServer(FastMCP):
    """天气查询 MCP 服务器"""

    def __init__(self):
        super().__init__(
            title="天气查询服务",
            description="提供全球城市天气信息查询服务",
            version="0.1.0",
        )

        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger("weather-mcp")

        # 初始化并注册天气工具
        weather_tools = WeatherTools(logger)
        weather_tools.register_tools(self)


def create_app() -> WeatherMCPServer:
    """
    创建并配置 MCP 服务器应用

    Returns:
        WeatherMCPServer: 配置好的 MCP 服务器实例
    """
    return WeatherMCPServer()


def main():
    """
    服务器入口点
    """
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
