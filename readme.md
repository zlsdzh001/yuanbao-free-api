# YuanBao-Free-API

YuanBao-Free-API 是一个允许您通过 OpenAI 兼容接口访问腾讯元宝大模型的服务。该项目包含服务端和客户端两部分，可以让您轻松地将腾讯元宝大模型集成到您的应用中。

## 功能特点

- 提供 OpenAI 兼容的 API 接口
- 支持多种元宝模型（deepseek-v3, deepseek-r1, hunyuan 等）
- 支持流式输出（Streaming）
- 支持网络搜索功能
- 简单易用的客户端示例

## 注意事项

- **本项目仅供学习和研究使用**
- **请遵守腾讯元宝的使用条款和条件**
- `hy_token` 有时效性，过期后需要重新获取

## 安装

1. 克隆仓库

```bash
git clone https://github.com/chenwr727/yuanbao-free-api.git
cd yuanbao-free-api
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 启动服务端

#### 本地部署

```bash
python app.py
```

服务将在 `http://localhost:8000` 启动。

#### Docker 部署

##### 构建镜像

```bash
docker build -t yuanbao-free-api .
```

##### 运行容器

```bash
docker run -d -p 8000:8000 --name yuanbao-api yuanbao-free-api
```

### 客户端

#### 参数获取

- `hy_user`、`agent_id` 和 `hy_token`（用于认证）需要从元宝网站获取。

![Token获取方法](example.png)

1. 登录 [腾讯元宝网站](https://yuanbao.tencent.com/)
2. 打开浏览器开发者工具（F12）
3. 在网络请求中找到对话请求，查看请求头中的 Cookie
4. 从 Cookie 中提取 `hy_user`、`hy_token` 值
5. 从请求中提取 `agent_id`

#### 使用 OpenAI SDK 调用

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1/", # 替换为服务端地址
    api_key="your_hy_token",  # 替换为 hy_token 
)

response = client.chat.completions.create(
    model="deepseek-r1-search",  # 支持的模型见 const.py
    messages=[{"role": "user", "content": "你是谁"}],
    stream=True,
    extra_body={
        "hy_source": "web",
        "hy_user": "your_hy_user",  # 替换为 hy_user
        "agent_id": "your_agent_id",  # 替换为 agent_id
        "chat_id": "your_chat_id",  # 可选，如果不提供会自动创建
        "should_remove_conversation": False,  # 是否在对话结束后删除会话
    },
)

for chunk in response:
    print(chunk.choices[0].delta.content or "")
```

## 支持的模型

目前支持以下模型：

- `deepseek-v3`：深度求索 V3 模型
- `deepseek-r1`：深度求索 R1 模型
- `deepseek-v3-search`：带搜索功能的深度求索 V3 模型
- `deepseek-r1-search`：带搜索功能的深度求索 R1 模型
- `hunyuan`：腾讯混元模型
- `hunyuan-t1`：腾讯混元 T1 模型
- `hunyuan-search`：带搜索功能的腾讯混元模型
- `hunyuan-t1-search`：带搜索功能的腾讯混元 T1 模型

## 许可证

MIT

## 贡献

欢迎提交 Issues 和 Pull Requests！