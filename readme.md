# YuanBao-Free-API ✨

一个允许您通过 OpenAI 兼容接口访问腾讯元宝的服务。

## ✨ 核心特性

✅ **完整兼容 OpenAI API 规范**  
🚀 **支持主流元宝大模型**（DeepSeek/HunYuan系列）  
⚡️ **流式输出 & 网络搜索功能**  
📦 **开箱即用的部署方案**（本地/Docker）  

## ⚠️ 使用须知

- 本项目仅限**学习研究用途**
- 请严格遵守腾讯元宝的[使用条款](https://yuanbao.tencent.com/)
- `hy_token` 有时效性，过期需重新获取

## 🚀 快速开始

### 环境准备
```bash
git clone https://github.com/chenwr727/yuanbao-free-api.git
cd yuanbao-free-api
pip install -r requirements.txt
```

## 🖥️ 服务端部署

### 本地运行
```bash
# 服务地址：http://localhost:8000
python app.py
```

### Docker部署
```bash
# 构建镜像
docker build -t yuanbao-free-api .

# 运行容器
docker run -d -p 8000:8000 --name yuanbao-api yuanbao-free-api
```

## 📡 客户端调用

### 认证参数获取
#### 手动获取
![Token获取方法](example.png)
1. 访问[腾讯元宝](https://yuanbao.tencent.com/)
2. 打开开发者工具（F12）
3. 捕获对话请求获取：
   - Cookie中的 `hy_user` 和 `hy_token`
   - 请求体中的 `agent_id`

#### 自动获取
```bash
# 扫码登录后自动输出认证参数
python get_cookies.py
```

### API调用示例
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

## 🧠 支持模型

| 模型名称              | 特性说明                    |
|----------------------|-----------------------------|
| deepseek-v3          | 深度求索 V3 基础模型         |
| deepseek-r1          | 深度求索 R1 增强模型         |
| deepseek-v3-search   | 深度求索 V3 模型（带搜索功能）|
| deepseek-r1-search   | 深度求索 R1 模型（带搜索功能）|
| hunyuan              | 腾讯混元基础模型             |
| hunyuan-t1           | 腾讯混元 T1 模型             |
| hunyuan-search       | 腾讯混元模型（带搜索功能）    |
| hunyuan-t1-search    | 腾讯混元 T1 模型（带搜索功能）|

## 🌟 应用案例

[FinVizAI](https://github.com/chenwr727/FinVizAI) 实现多步骤金融分析工作流：
- 实时资讯搜索分析
- 市场趋势数据集成
- 结构化报告生成

## 📜 开源协议

MIT License © 2025

## 🤝 参与贡献

欢迎通过以下方式参与项目：
1. 提交Issue报告问题
2. 创建Pull Request贡献代码
3. 分享你的集成案例