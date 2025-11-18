"""
Gradio Web UI for DeepSeek Chat Agent (API调用方案)
分离方案：通过 HTTP 调用 main.py 的 API 接口
需要先启动 main.py 服务
"""
import gradio as gr
import requests
import json
from typing import List, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API 配置
API_BASE_URL = "http://localhost:8080"
API_CHAT_ENDPOINT = f"{API_BASE_URL}/api/chat"


class ChatBot:
    """聊天机器人类，通过 API 调用生成回复"""

    def __init__(self):
        """初始化聊天机器人"""
        self.message_log = [{"role": "ai", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}]
        self.conversation_history = []  # 存储完整的对话历史

    def generate_ai_response(self, user_input: str, temperature: float = 0.7) -> str:
        """
        通过 API 调用生成AI回复
        
        Args:
            user_input: 用户输入
            temperature: 温度参数
            
        Returns:
            AI回复内容
        """
        try:
            # 添加用户消息到对话历史
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # 构建请求数据
            request_data = {
                "messages": self.conversation_history,
                "temperature": temperature,
                "max_tokens": 5000
            }
            
            # 发送 POST 请求
            response = requests.post(
                API_CHAT_ENDPOINT,
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=60  # 60秒超时
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            ai_message = result.get("message", "抱歉，无法获取回复。")
            
            # 添加AI回复到对话历史
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
            
        except requests.exceptions.ConnectionError:
            error_msg = "❌ 无法连接到 API 服务。请确保 main.py 服务正在运行（python -m app.main）"
            logger.error(error_msg)
            return error_msg
            
        except requests.exceptions.Timeout:
            error_msg = "⏱️ 请求超时，请稍后重试。"
            logger.error(error_msg)
            return error_msg
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"❌ HTTP 错误: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"❌ 发生错误: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg

    def chat(self, message: str, temperature: float, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        """
        处理聊天消息
        
        Args:
            message: 用户消息
            temperature: 温度参数
            history: Gradio聊天历史
            
        Returns:
            (空字符串, 更新后的历史记录)
        """
        if not message or not message.strip():
            return "", history
        
        # 添加用户消息到日志
        self.message_log.append({"role": "user", "content": message})
        
        # 生成AI回复
        ai_response = self.generate_ai_response(message, temperature)
        
        # 添加AI回复到日志
        self.message_log.append({"role": "ai", "content": ai_response})
        
        # 更新Gradio聊天历史
        history.append((message, ai_response))
        
        return "", history

    def clear_history(self) -> List[Tuple[str, str]]:
        """清空聊天历史"""
        self.conversation_history = []
        self.message_log = [{"role": "ai", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}]
        return []

    def check_api_health(self) -> bool:
        """检查 API 服务是否可用"""
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            return response.status_code == 200
        except:
            return False


def create_demo():
    """创建Gradio演示界面"""
    chatbot = ChatBot()
    
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="blue", neutral_hue="zinc"),
        title="DeepSeek Chat Agent (API Mode)"
    ) as demo:
        # 标题和描述
        gr.Markdown("# 🧠 DeepSeek Chat Agent")
        gr.Markdown("🚀 基于 LangChain 和 DeepSeek API 的智能聊天助手 (API调用模式)")
        
        # API 状态检查
        with gr.Row():
            api_status = gr.Markdown(
                value="🟢 API 服务状态：检查中...",
                visible=True
            )
        
        def check_status():
            """检查API状态"""
            if chatbot.check_api_health():
                return "🟢 API 服务状态：正常运行"
            else:
                return "🔴 API 服务状态：未连接（请先运行: python -m app.main）"
        
        # 初始状态检查
        initial_status = check_status()
        api_status.value = initial_status
        
        with gr.Row():
            # 左侧：聊天区域
            with gr.Column(scale=4):
                chatbot_component = gr.Chatbot(
                    value=[(None, "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻")],
                    height=500,
                    label="对话历史",
                    show_label=True,
                    container=True,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="在这里输入你的问题...",
                        show_label=False,
                        scale=9,
                        container=False
                    )
                    submit_btn = gr.Button("发送", variant="primary", scale=1)
                    clear_btn = gr.Button("清空", variant="secondary", scale=1)
                    refresh_btn = gr.Button("刷新状态", variant="secondary", scale=1)
                
            # 右侧：配置区域
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ 配置")
                
                temperature_slider = gr.Slider(
                    minimum=0.0,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature (温度)",
                    info="控制回复的随机性，值越高越随机"
                )
                
                gr.Markdown("### 📋 功能特性")
                gr.Markdown("""
                - 🐍 Python 编程助手
                - 🐞 代码调试支持
                - 📝 代码文档生成
                - 💡 解决方案设计
                - 🔍 问题分析
                """)
                
                gr.Markdown("### 🔗 技术栈")
                gr.Markdown("""
                - [DeepSeek API](https://www.deepseek.com/)
                - [LangChain](https://python.langchain.com/)
                - [Gradio](https://gradio.app/)
                - FastAPI (后端服务)
                """)
                
                gr.Markdown("### 📊 API 信息")
                gr.Markdown(f"""
                - **API地址**: {API_BASE_URL}
                - **端点**: /api/chat
                - **最大Tokens**: 5000
                """)
        
        # 绑定事件
        msg.submit(
            fn=chatbot.chat,
            inputs=[msg, temperature_slider, chatbot_component],
            outputs=[msg, chatbot_component]
        )
        
        submit_btn.click(
            fn=chatbot.chat,
            inputs=[msg, temperature_slider, chatbot_component],
            outputs=[msg, chatbot_component]
        )
        
        clear_btn.click(
            fn=chatbot.clear_history,
            inputs=[],
            outputs=[chatbot_component]
        )
        
        refresh_btn.click(
            fn=check_status,
            inputs=[],
            outputs=[api_status]
        )
    
    return demo


if __name__ == "__main__":
    # 创建并启动Gradio应用
    demo = create_demo()
    
    # 启动应用
    demo.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,        # Gradio默认端口
        share=False,             # 设置为True可以生成公共链接
        show_error=True          # 显示详细错误信息
    )

