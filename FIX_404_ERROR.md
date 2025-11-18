# 修复 404 错误指南

## 🔍 问题原因

出现 "Error code: 404" 错误的主要原因是：

1. **API Base URL 不正确**
   - 之前使用：`https://api.deepseek.com`
   - 正确应该是：`https://api.deepseek.com/v1`

2. **参数名错误**
   - 之前使用：`base_url`
   - 正确应该是：`api_base`

## ✅ 已修复的内容

### 1. 修复了 `app/gradio_app.py`

**之前：**
```python
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")

llm = ChatDeepSeek(
    ...
    base_url=DEEPSEEK_API_BASE  # ❌ 错误的参数名
)
```

**现在：**
```python
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

llm = ChatDeepSeek(
    ...
    api_base=DEEPSEEK_API_BASE  # ✅ 正确的参数名和端点
)
```

### 2. 修复了 `app/main.py`

同样的问题和修复。

### 3. 改进了错误处理

现在会提供更友好的错误信息：
- 404 错误：提示检查 API Key、Base URL 和模型名称
- 401 错误：提示检查 API Key
- 429 错误：提示请求频率过高
- 其他错误：提供通用检查建议

## 🔧 如何验证修复

### 步骤 1：检查 .env 文件

确保 `.env` 文件中的配置正确：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

**注意：** 如果 `.env` 文件中没有 `DEEPSEEK_API_BASE`，代码会自动使用正确的默认值。

### 步骤 2：重启应用

```powershell
# 停止当前运行的应用（Ctrl+C）
# 然后重新启动

# Gradio UI
python -m app.gradio_app

# 或 FastAPI
python -m app.main
```

### 步骤 3：测试

在 Gradio UI 中输入一个问题，应该能正常获得回复。

## 📋 常见问题

### Q: 如果还是出现 404 错误怎么办？

**A:** 请检查以下几点：

1. **确认 API Key 有效**
   - 访问 [DeepSeek 官网](https://www.deepseek.com/) 检查 API Key
   - 确保 API Key 没有过期或被禁用

2. **检查网络连接**
   - 确保能访问 `https://api.deepseek.com`
   - 如果在国内，可能需要配置代理

3. **检查模型名称**
   - 确保使用 `deepseek-chat`（这是正确的模型名称）

4. **查看详细日志**
   - 检查控制台输出的详细错误信息
   - 查看日志文件（如果有）

### Q: 如何确认 API Base URL 是否正确？

**A:** 根据 `langchain-deepseek` 包的源码，正确的配置是：

```python
DEFAULT_API_BASE = "https://api.deepseek.com/v1"
```

所以应该使用 `https://api.deepseek.com/v1`，而不是 `https://api.deepseek.com`。

### Q: 参数名为什么是 `api_base` 而不是 `base_url`？

**A:** 这是 `langchain-deepseek` 包定义的参数名。查看包的源码可以看到：

```python
api_base: str = Field(
    default_factory=from_env("DEEPSEEK_API_BASE", default=DEFAULT_API_BASE),
)
```

所以必须使用 `api_base` 参数名。

## 🎯 验证修复是否成功

运行以下测试：

```python
# 测试代码
from langchain_deepseek import ChatDeepSeek
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base="https://api.deepseek.com/v1"  # 正确的配置
)

# 测试调用
response = llm.invoke("你好")
print(response.content)
```

如果这个测试成功，说明配置正确。

## 📚 相关文档

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [langchain-deepseek 文档](https://python.langchain.com/docs/integrations/chat/deepseek)

## ✅ 修复完成

现在应该可以正常使用了！如果还有问题，请查看错误日志获取更多信息。

