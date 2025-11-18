# API 使用指南

## `/api/chat` 接口使用说明

`/api/chat` 是一个 **POST** 接口，不能直接在浏览器地址栏访问（浏览器默认是 GET 请求）。以下是多种使用方式：

---

## 方法 1：使用 FastAPI Swagger UI（最简单，推荐）⭐

### 步骤：

1. **启动服务**
   ```powershell
   python -m app.main
   ```

2. **打开浏览器访问 Swagger UI**
   ```
   http://localhost:8080/docs
   ```

3. **在 Swagger UI 中操作：**
   - 找到 `POST /api/chat` 接口
   - 点击 "Try it out" 按钮
   - 在 "Request body" 中输入 JSON 数据（示例见下方）
   - 点击 "Execute" 按钮
   - 查看响应结果

### 请求示例（在 Swagger UI 的 Request body 中）：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "你好，请介绍一下你自己"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 5000
}
```

### 完整对话示例：

```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个专业的Python编程助手"
    },
    {
      "role": "user",
      "content": "如何创建一个Python虚拟环境？"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

---

## 方法 2：使用浏览器扩展（REST Client）

### 安装扩展：
- Chrome/Edge: 安装 "REST Client" 或 "Talend API Tester" 扩展
- Firefox: 安装 "RESTClient" 扩展

### 使用步骤：
1. 打开扩展
2. 选择 POST 方法
3. 输入 URL: `http://localhost:8080/api/chat`
4. 设置 Headers: `Content-Type: application/json`
5. 在 Body 中输入 JSON 数据
6. 点击发送

---

## 方法 3：使用 curl 命令（命令行）

### Windows PowerShell:

```powershell
curl -X POST "http://localhost:8080/api/chat" `
  -H "Content-Type: application/json" `
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 5000
  }'
```

### Windows CMD:

```cmd
curl -X POST "http://localhost:8080/api/chat" -H "Content-Type: application/json" -d "{\"messages\": [{\"role\": \"user\", \"content\": \"你好，请介绍一下你自己\"}], \"temperature\": 0.7, \"max_tokens\": 5000}"
```

### Linux/macOS:

```bash
curl -X POST "http://localhost:8080/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 5000
  }'
```

---

## 方法 4：使用 Python requests

### 创建测试脚本 `test_chat.py`:

```python
import requests
import json

# API 地址
url = "http://localhost:8080/api/chat"

# 请求数据
data = {
    "messages": [
        {
            "role": "user",
            "content": "你好，请介绍一下你自己"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 5000
}

# 发送请求
response = requests.post(url, json=data)

# 打印响应
print("状态码:", response.status_code)
print("响应内容:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 运行：

```powershell
python test_chat.py
```

---

## 方法 5：使用 Postman

### 步骤：

1. **打开 Postman**
2. **创建新请求**
   - 方法：选择 `POST`
   - URL：输入 `http://localhost:8080/api/chat`
3. **设置 Headers**
   - Key: `Content-Type`
   - Value: `application/json`
4. **设置 Body**
   - 选择 `raw`
   - 选择 `JSON`
   - 输入 JSON 数据（见示例）
5. **点击 Send**

---

## 方法 6：使用 JavaScript (浏览器控制台)

在浏览器控制台（F12）中运行：

```javascript
fetch('http://localhost:8080/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    messages: [
      {
        role: 'user',
        content: '你好，请介绍一下你自己'
      }
    ],
    temperature: 0.7,
    max_tokens: 5000
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## 请求参数说明

### 请求体 (JSON)：

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `messages` | Array | 是 | 消息列表 | 见下方 |
| `temperature` | Float | 否 | 温度参数 (0.0-2.0)，默认 0.7 | 0.7 |
| `max_tokens` | Integer | 否 | 最大token数 (1-5000)，默认 5000 | 1000 |

### messages 数组中的消息对象：

| 字段 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| `role` | String | 是 | 消息角色 | `user`, `assistant`, `system` |
| `content` | String | 是 | 消息内容 | 任意文本 |

---

## 响应格式

### 成功响应 (200)：

```json
{
  "message": "你好！我是DeepSeek，一个AI助手...",
  "usage": {
    "estimated_tokens": 150,
    "max_tokens": 5000
  }
}
```

### 错误响应 (500)：

```json
{
  "detail": "处理请求时出错: ..."
}
```

---

## 完整示例

### 示例 1：简单对话

**请求：**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "什么是Python？"
    }
  ]
}
```

### 示例 2：带系统提示的对话

**请求：**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个专业的Python编程助手，请用简洁明了的方式回答问题。"
    },
    {
      "role": "user",
      "content": "如何创建一个列表？"
    }
  ],
  "temperature": 0.5,
  "max_tokens": 500
}
```

### 示例 3：多轮对话

**请求：**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Python中如何读取文件？"
    },
    {
      "role": "assistant",
      "content": "在Python中，可以使用open()函数读取文件..."
    },
    {
      "role": "user",
      "content": "能给我一个完整的示例吗？"
    }
  ]
}
```

---

## 快速测试

### 1. 健康检查（GET 请求，可直接在浏览器访问）

```
http://localhost:8080/health
```

或

```
http://localhost:8080/
```

### 2. API 文档（可直接在浏览器访问）

```
http://localhost:8080/docs
```

### 3. 简化版聊天接口（GET 请求，可直接在浏览器访问）

```
http://localhost:8080/api/chat/simple?user_input=你好
```

---

## 常见问题

### Q: 为什么直接在浏览器访问 `http://localhost:8080/api/chat` 会出错？

A: 因为这是一个 POST 接口，需要发送 JSON 数据。浏览器地址栏只能发送 GET 请求。请使用上述方法之一。

### Q: 如何查看所有可用的接口？

A: 访问 `http://localhost:8080/docs` 查看完整的 API 文档。

### Q: 如何测试接口是否正常工作？

A: 先访问 `http://localhost:8080/health` 检查服务是否运行，然后使用 Swagger UI (`/docs`) 测试接口。

---

## 推荐使用方式

**对于初学者：** 使用方法 1（Swagger UI），最简单直观  
**对于开发者：** 使用方法 4（Python requests），便于集成到代码中  
**对于测试：** 使用方法 5（Postman），功能强大

