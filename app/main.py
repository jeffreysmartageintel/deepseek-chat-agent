"""
FastAPI application for DeepSeek Chat Agent
使用LangChain集成DeepSeek API，提供聊天接口
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv
import logging

# 导入 ChatDeepSeek（使用 langchain-deepseek 包）
from langchain_deepseek import ChatDeepSeek

# 导入消息类型
try:
    from langchain.schema import HumanMessage, AIMessage, SystemMessage
except ImportError:
    try:
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    except ImportError:
        raise ImportError("无法导入 LangChain 消息类型，请检查 LangChain 安装")

# 加载 .env 文件（如果存在）
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DeepSeek Chat Agent API",
    description="基于LangChain和DeepSeek的聊天API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量获取API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

# 初始化DeepSeek模型
# DeepSeek API endpoint - 注意：应该是 /v1 端点
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

# 初始化 ChatDeepSeek 模型
# 注意：参数名是 api_base，不是 base_url
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=5000,  # 控制token在5000以内
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_API_BASE  # 使用 api_base 而不是 base_url
)
logger.info("Initialized ChatDeepSeek model")


# 请求模型
class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色: user, assistant, system")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="聊天消息列表")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="温度参数")
    max_tokens: Optional[int] = Field(5000, ge=1, le=5000, description="最大token数")


class ChatResponse(BaseModel):
    message: str = Field(..., description="AI回复内容")
    usage: Optional[dict] = Field(None, description="Token使用情况")


@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "DeepSeek Chat Agent",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口
    
    接收用户消息，调用DeepSeek模型，返回AI回复
    """
    try:
        # 确保max_tokens不超过5000
        max_tokens = min(request.max_tokens or 5000, 5000)
        
        # 转换消息格式为LangChain格式
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        
        # 如果没有system消息，添加默认的
        if not any(isinstance(m, SystemMessage) for m in langchain_messages):
            langchain_messages.insert(0, SystemMessage(content="你是一个有用的AI助手。"))
        
        logger.info(f"Processing chat request with {len(langchain_messages)} messages")
        
        # 调用模型
        if hasattr(llm, 'invoke'):
            # ChatDeepSeek使用invoke方法
            response = llm.invoke(langchain_messages)
            ai_message = response.content if hasattr(response, 'content') else str(response)
        else:
            # DeepSeek LLM使用generate或直接调用
            # 将消息列表转换为字符串
            prompt = "\n".join([f"{m.__class__.__name__}: {m.content}" for m in langchain_messages])
            response = llm(prompt)
            ai_message = str(response)
        
        # 估算token使用（简单估算，实际应该从API响应中获取）
        # 这里使用简单的字符数估算（1 token ≈ 4 characters for Chinese）
        estimated_tokens = len(ai_message) // 4 + len("".join([m.content for m in langchain_messages])) // 4
        
        logger.info(f"Generated response with estimated {estimated_tokens} tokens")
        
        return ChatResponse(
            message=ai_message,
            usage={
                "estimated_tokens": estimated_tokens,
                "max_tokens": max_tokens
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")


@app.post("/api/chat/simple")
async def chat_simple(user_input: str=Query(..., description="用户输入的问题")):
    """
    简化版聊天接口
    
    直接接收用户输入字符串，返回AI回复
    """
    try:
        # 创建简单的用户消息
        messages = [
            ChatMessage(role="user", content=user_input)
        ]
        
        request = ChatRequest(messages=messages)
        response = await chat(request)
        
        return {
            "user_input": user_input,
            "ai_response": response.message,
            "usage": response.usage
        }
        
    except Exception as e:
        logger.error(f"Error in simple chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

