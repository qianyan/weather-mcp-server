# 天气 MCP 服务器

这是一个基于 FastMCP 构建的天气查询服务器，提供城市天气信息查询服务。

## 功能特点

- 支持全球城市天气查询
- 提供温度、湿度和天气描述信息
- 支持摄氏度和华氏度温度单位切换
- 基于 Model Context Protocol (MCP) 实现
- 完整的日志记录

## 安装要求

- Python 3.8+
- OpenWeatherMap API 密钥
- uv (Python 包管理工具)

## 快速开始

1. 克隆仓库：
```bash
git clone <repository-url>
cd weather-mcp-server
```

2. 安装依赖：
```bash
make install
```

3. 设置环境变量：
创建 `.env` 文件并添加以下内容：
```
OPENWEATHER_API_KEY=你的OpenWeatherMap_API密钥
```

4. 运行服务器：
```bash
make run
```

## 安装和使用

### 选项 1：使用 uvx（推荐）

使用 `uvx` 将自动从 PyPI 安装包，无需克隆仓库。将以下配置添加到 Claude Desktop 的配置文件 `claude_desktop_config.json` 中：

```json
{
  "mcpServers": {
    "weather-mcp-server": {
      "command": "uvx",
      "args": [
        "weather-mcp-server"
      ],
      "env": {
        "OPENWEATHER_API_KEY": "你的OpenWeatherMap_API密钥"
      }
    }
  }
}
```

### 选项 2：本地开发模式

1. 克隆仓库并安装依赖：
```bash
git clone <repository-url>
cd weather-mcp-server
make install
```

2. 设置环境变量：
创建 `.env` 文件并添加以下内容：
```
OPENWEATHER_API_KEY=你的OpenWeatherMap_API密钥
```

3. 在 Claude Desktop 配置文件中添加：
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/src/weather_mcp_server",
        "run",
        "weather-mcp-server"
      ],
      "env": {
        "OPENWEATHER_API_KEY": "你的OpenWeatherMap_API密钥"
      }
    }
  }
}
```

配置文件位置：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

重启 Claude Desktop 以加载新的 MCP 服务器。

## 开发

本项目使用 Makefile 来简化常用命令。

### 可用命令

```bash
make install  # 安装依赖
make format   # 格式化代码
make lint     # 运行代码检查
make clean    # 清理临时文件
make run      # 运行服务器
```

### 发布新版本

```bash
make release version=v0.1.0
```

## MCP 工具

服务器提供以下 MCP 工具：

### get_weather

获取指定城市的天气信息。

参数：
- `city`: 城市名称（必填）
- `units`: 温度单位（可选，默认为 "metric"）
  - "metric": 摄氏度
  - "imperial": 华氏度

示例请求：
```json
{
    "name": "get_weather",
    "kwargs": {
        "city": "Beijing",
        "units": "metric"
    }
}
```

示例响应：
```json
{
    "temperature": 20.5,
    "humidity": 65,
    "description": "晴",
    "city": "Beijing"
}
```

现在您可以通过 Claude 使用自然语言命令与天气服务进行交互，例如：
- "查看北京的天气"
- "东京现在的温度是多少"
- "伦敦的天气情况如何" 