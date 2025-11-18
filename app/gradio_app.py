"""
Gradio Web UI for DeepSeek Chat Agent
集成方案：直接使用 main.py 中的 LLM，无需通过 HTTP API
"""
import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
import logging

# 导入 main.py 中的 LLM 初始化逻辑
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

# DeepSeek API base URL - 注意：应该是 /v1 端点
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

# 初始化 ChatDeepSeek 模型（与 main.py 保持一致）
# 注意：参数名是 api_base，不是 base_url
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=5000,
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_API_BASE  # 使用 api_base 而不是 base_url
)
logger.info("Initialized ChatDeepSeek model for Gradio UI")

# 系统提示配置
SYSTEM_TEMPLATE = """你是一个专业的AI编程助手。提供简洁、正确的解决方案，并包含用于调试的策略性打印语句。请用中文回答。"""

# 创建聊天提示模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_TEMPLATE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


class ChatBot:
    """聊天机器人类，管理对话历史和生成回复"""

    def __init__(self):
        """初始化聊天机器人"""
        self.chat_history = []
        # 使用新的 messages 格式（OpenAI 风格）
        self.message_log = [{"role": "assistant", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}]

    def generate_ai_response(self, user_input: str, temperature: float=0.7):
        """
        生成AI回复
        
        Args:
            user_input: 用户输入
            temperature: 温度参数，控制回复的随机性
            
        Returns:
            AI回复内容
        """
        try:
            # 添加用户消息到聊天历史
            self.chat_history.append(HumanMessage(content=user_input))
            
            # 如果设置了温度，更新LLM配置
            if temperature != 0.7:
                llm.temperature = temperature
            
            # 构建对话链
            chain = chat_prompt | llm | StrOutputParser()
            
            # 生成回复
            response = chain.invoke({
                "input": user_input,
                "chat_history": self.chat_history[:-1]  # 不包含当前用户消息
            })
            
            # 添加AI回复到聊天历史
            self.chat_history.append(AIMessage(content=response))
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating AI response: {error_msg}", exc_info=True)
            
            # 提供更友好的错误信息
            if "404" in error_msg or "Not Found" in error_msg:
                return f"❌ API 端点错误 (404)。请检查：\n1. API Key 是否正确\n2. API Base URL 是否正确（应该是 https://api.deepseek.com/v1）\n3. 模型名称是否正确（deepseek-chat）\n\n详细错误：{error_msg}"
            elif "401" in error_msg or "Unauthorized" in error_msg:
                return f"❌ API Key 无效 (401)。请检查 .env 文件中的 DEEPSEEK_API_KEY 是否正确。\n\n详细错误：{error_msg}"
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                return f"⏱️ API 请求频率过高 (429)。请稍后再试。\n\n详细错误：{error_msg}"
            else:
                return f"❌ 生成回复时出现错误：{error_msg}\n\n请检查：\n1. 网络连接是否正常\n2. API Key 是否有效\n3. API 服务是否可用"

    def chat(self, message: str, temperature: float, history: list):
        """
        处理聊天消息
        
        Args:
            message: 用户消息
            temperature: 温度参数
            history: Gradio聊天历史（messages 格式）
            
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
        self.message_log.append({"role": "assistant", "content": ai_response})
        
        # 更新Gradio聊天历史（使用 messages 格式）
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": ai_response})
        
        return "", history

    def clear_history(self):
        """清空聊天历史"""
        self.chat_history = []
        # 使用新的 messages 格式
        self.message_log = [{"role": "assistant", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}]
        return [{"role": "assistant", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}]


def create_demo():
    """创建Gradio演示界面"""
    chatbot = ChatBot()
    
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="blue", neutral_hue="zinc"),
        title="DeepSeek Chat Agent"
    ) as demo:
        # 标题和描述
        gr.Markdown("# 🧠 DeepSeek Chat Agent")
        gr.Markdown("🚀 基于 LangChain 和 DeepSeek API 的智能聊天助手")
        
        with gr.Row():
            # 左侧：聊天区域
            with gr.Column(scale=4):
                chatbot_component = gr.Chatbot(
                    value=[{"role": "assistant", "content": "你好！我是 DeepSeek AI 助手。我可以帮助你解决编程问题、调试代码、编写文档等。有什么我可以帮助你的吗？💻"}],
                    height=500,
                    label="对话历史",
                    show_label=True,
                    container=True,
                    type="messages"  # 使用新的 messages 格式（OpenAI 风格）
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
                """)
                
                gr.Markdown("### 📊 模型信息")
                gr.Markdown(f"""
                - **模型**: deepseek-chat
                - **最大Tokens**: 5000
                - **API**: {DEEPSEEK_API_BASE}
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
    
    return demo


if __name__ == "__main__":
    # 创建并启动Gradio应用
    demo = create_demo()
    
    # 获取端口（Google Cloud Run 会设置 PORT 环境变量）
    port = int(os.getenv("PORT", 8080))
    
    # 启动应用
    # share=False 在 Cloud Run 上不需要，因为已经有公共 URL
    demo.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=port,  # 使用环境变量 PORT 或默认 8080
        share=False,  # Cloud Run 不需要 share
        show_error=True,  # 显示详细错误信息
        show_api=False  # 在 Cloud Run 上不需要显示 API 文档
    )

