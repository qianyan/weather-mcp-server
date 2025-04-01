"""Weather MCP Server package."""

from .server import WeatherMCPServer as server

def main():
    """Main entry point for the package."""
    server.main()


__version__ = "0.1.0"
__all__ = ["main", "server"]
