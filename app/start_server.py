"""
启动脚本：用于 Cloud Run 部署
确保应用正确启动并监听端口
"""
# 兼容性修复：处理 huggingface_hub HfFolder 导入问题
# 在导入 gradio_app 之前修复，避免导入错误
try:
    import huggingface_hub
    # 如果 HfFolder 不存在，创建一个兼容的类
    if not hasattr(huggingface_hub, 'HfFolder'):

        class HfFolder:
            """兼容性类，替代已移除的 HfFolder"""

            @staticmethod
            def save_token(token: str):
                """保存 token 的占位方法"""
                pass
            
            @staticmethod
            def get_token():
                """获取 token 的占位方法"""
                return None

        huggingface_hub.HfFolder = HfFolder
except ImportError:
    pass

import os
import sys
import logging
from dotenv import load_dotenv

# 加载 .env 文件（必须在检查环境变量之前）
load_dotenv()

# 配置日志 - 立即输出，不缓冲
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置
)
logger = logging.getLogger(__name__)


def main():
    """主启动函数"""
    try:
        # 获取端口
        port = int(os.getenv("PORT", 8080))
        logger.info("=" * 50)
        logger.info("Starting DeepSeek Chat Agent - Gradio UI")
        logger.info(f"Port: {port}")
        logger.info("=" * 50)
        
        # 验证环境变量
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            logger.error("DEEPSEEK_API_KEY environment variable is not set")
            sys.exit(1)
        logger.info("✓ DEEPSEEK_API_KEY is set")
        
        api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
        logger.info(f"✓ DEEPSEEK_API_BASE: {api_base}")
        
        # 导入并启动 Gradio 应用
        # 直接启动 Gradio，不使用健康检查服务器
        # Gradio 启动后会立即监听端口，满足 Cloud Run 的要求
        logger.info("Importing Gradio app module...")
        try:
            from app.gradio_app import create_demo
            logger.info("✓ Gradio module imported successfully")
        except Exception as e:
            logger.error(f"Failed to import Gradio app: {e}", exc_info=True)
            raise
        
        logger.info("Creating Gradio demo interface...")
        try:
            demo = create_demo()
            logger.info("✓ Gradio demo created successfully")
        except Exception as e:
            logger.error(f"Failed to create Gradio demo: {e}", exc_info=True)
            raise
        
        logger.info(f"Launching Gradio server on 0.0.0.0:{port}")
        logger.info("This may take a few seconds...")
        
        # 启动 Gradio - 使用阻塞模式
        # 重要：server_name 必须是 "0.0.0.0" 才能从外部访问
        # root_path 设置：
        # - 本地开发：不设置或设置为 None（避免 URL 出现双斜杠）
        # - Cloud Run 部署：设置为 "/" 或根据实际路径设置
        root_path = os.getenv("GRADIO_ROOT_PATH", None)
        if root_path == "":
            root_path = None
        
        # 启动 Gradio（阻塞调用，会一直运行）
        # 注意：launch() 会阻塞，直到容器停止
        demo.launch(
            server_name="0.0.0.0",  # 必须绑定到 0.0.0.0，不能是 127.0.0.1 或 localhost
            server_port=port,
            share=False,
            show_error=True,
            show_api=False,
            prevent_thread_lock=False,  # False = 阻塞模式，保持容器运行
            inbrowser=False,
            root_path=root_path,  # 本地开发时不设置，避免 URL 双斜杠问题
            favicon_path=None,  # 禁用 favicon 加载，加快启动
            quiet=False  # 显示启动信息
        )
        
        # 这行代码不会被执行，因为 launch() 会阻塞
        logger.info("Gradio server started successfully")
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

