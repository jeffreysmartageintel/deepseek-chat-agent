# 本地测试指南 - start_server.py

## 前置条件

### 1. 检查 Python 环境

```powershell
# 检查 Python 版本（需要 3.11+）
python --version

# 检查是否在虚拟环境中
# 如果显示 (venv) 或类似前缀，说明在虚拟环境中
```

### 2. 安装依赖

```powershell
# 如果还没有虚拟环境，创建并激活
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

确保 `.env` 文件存在并包含以下内容：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
# GRADIO_ROOT_PATH=  # 本地测试时可以不设置或留空
```

**注意**：将 `your_api_key_here` 替换为实际的 DeepSeek API Key。

---

## 本地测试步骤

### 方法 1: 直接运行 start_server.py（推荐）

```powershell
# 确保在项目根目录
cd D:\smartage-code\deepseek-chat-agent

# 激活虚拟环境（如果使用）
.\venv\Scripts\Activate.ps1

# 运行启动脚本
python -m app.start_server
```

### 方法 2: 使用 Python 模块方式

```powershell
# 在项目根目录运行
python -m app.start_server
```

### 方法 3: 设置 PORT 环境变量（如果需要使用其他端口）

```powershell
# Windows PowerShell
$env:PORT=8080
python -m app.start_server

# 或者一行命令
$env:PORT=8080; python -m app.start_server
```

---

## 预期输出

如果一切正常，应该看到类似以下输出：

```
==================================================
Starting DeepSeek Chat Agent - Gradio UI
Port: 8080
==================================================
✓ DEEPSEEK_API_KEY is set
✓ DEEPSEEK_API_BASE: https://api.deepseek.com/v1
Importing Gradio app module...
✓ Gradio module imported successfully
Creating Gradio demo interface...
✓ Gradio demo created successfully
Launching Gradio server on 0.0.0.0:8080
This may take a few seconds...
Running on local URL:  http://127.0.0.1:8080
```

---

## 访问应用

启动成功后，在浏览器中访问：

```
http://localhost:8080
```

**应该看到**：
- ✅ Gradio 聊天界面
- ✅ 聊天历史区域
- ✅ 输入框和发送按钮
- ✅ 清除按钮
- ✅ 温度滑块

---

## 测试功能

### 1. 基本聊天测试

1. 在输入框中输入问题，例如：`你好，介绍一下你自己`
2. 点击 **"发送"** 按钮
3. 等待 AI 回复
4. 确认回复正常显示

### 2. 温度参数测试

1. 调整温度滑块（0.0 - 2.0）
2. 输入相同的问题
3. 观察回复的变化（温度越高，回复越随机）

### 3. 清除聊天历史

1. 点击 **"清除"** 按钮
2. 确认聊天历史被清空

---

## 常见问题

### Q1: 错误 `DEEPSEEK_API_KEY environment variable is not set`

**原因**：`.env` 文件不存在或未正确配置

**解决**：
1. 检查 `.env` 文件是否存在
2. 确认 `DEEPSEEK_API_KEY` 已设置
3. 确认 `.env` 文件在项目根目录

### Q2: 错误 `ModuleNotFoundError: No module named 'app'`

**原因**：不在项目根目录运行，或未安装依赖

**解决**：
```powershell
# 确保在项目根目录
cd D:\smartage-code\deepseek-chat-agent

# 安装依赖
pip install -r requirements.txt
```

### Q3: 错误 `ImportError: cannot import name 'HfFolder'`

**原因**：Gradio 版本兼容性问题

**解决**：
- 代码中已包含兼容性修复，如果仍有问题，检查 `requirements.txt` 中的 Gradio 版本

### Q4: 访问 `http://localhost:8080` 显示 "无法访问此网站"

**原因**：
1. 服务器未启动
2. 端口被占用
3. 防火墙阻止

**解决**：
```powershell
# 检查端口是否被占用
netstat -ano | findstr :8080

# 如果端口被占用，使用其他端口
$env:PORT=8081
python -m app.start_server
```

### Q5: 页面显示 "加载中" 或空白

**原因**：
1. Gradio 启动中（需要几秒钟）
2. 浏览器缓存问题

**解决**：
1. 等待几秒钟后刷新页面
2. 清除浏览器缓存
3. 查看终端输出，确认 Gradio 是否正常启动

---

## 调试技巧

### 1. 查看详细日志

代码已配置日志输出，所有信息会显示在终端中。

### 2. 检查环境变量

```powershell
# 检查环境变量是否加载
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', os.getenv('DEEPSEEK_API_KEY')[:10] + '...' if os.getenv('DEEPSEEK_API_KEY') else 'Not set')"
```

### 3. 测试 API 调用

如果 Gradio 界面正常，但无法收到回复：

1. 检查 `DEEPSEEK_API_KEY` 是否正确
2. 检查网络连接
3. 查看终端错误信息

---

## 停止服务器

在终端中按 `Ctrl + C` 停止服务器。

---

## 验证清单

测试完成后，确认：

- [ ] 服务器正常启动，无错误信息
- [ ] 可以访问 `http://localhost:8080`
- [ ] 看到 Gradio 聊天界面（不是 JSON）
- [ ] 可以输入问题并收到回复
- [ ] 温度滑块可以调整
- [ ] 清除按钮可以清空聊天历史

---

## 下一步

本地测试成功后：

1. **提交代码**（如果还没有）：
   ```powershell
   git add .
   git commit -m "Test start_server.py locally - working"
   git push
   ```

2. **部署到 Cloud Run**：
   - 使用 GitHub Actions 自动部署
   - 或手动部署（参考 `QUICK_DEPLOY.md`）

3. **验证 Cloud Run 部署**：
   - 访问 Cloud Run 服务 URL
   - 确认看到 Gradio 聊天界面（不是 JSON）

---

## 快速测试命令（一键运行）

```powershell
# 在项目根目录执行
# 确保虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 运行测试
python -m app.start_server
```

然后在浏览器中访问：`http://localhost:8080`

