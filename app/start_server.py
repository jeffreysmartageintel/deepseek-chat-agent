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
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
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

# 全局变量：健康检查服务器
health_server = None
health_server_thread = None


class HealthCheckHandler(BaseHTTPRequestHandler):
    """简单的健康检查处理器"""
    
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","service":"deepseek-chat-agent"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # 禁用默认日志输出，避免干扰
        pass


def start_health_check_server(port):
    """启动健康检查服务器（在后台线程中）"""
    global health_server, health_server_thread
    
    def run_server():
        global health_server
        try:
            health_server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
            logger.info(f"✓ Health check server started on port {port}")
            health_server.serve_forever()
        except Exception as e:
            logger.error(f"Health check server error: {e}")
    
    health_server_thread = threading.Thread(target=run_server, daemon=True)
    health_server_thread.start()
    time.sleep(0.5)  # 给服务器一点时间启动
    return health_server_thread


def main():
    """主启动函数"""
    global health_server
    
    try:
        # 获取端口
        port = int(os.getenv("PORT", 8080))
        logger.info("=" * 50)
        logger.info("Starting DeepSeek Chat Agent")
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
        
        # 立即启动健康检查服务器（让 Cloud Run 知道容器已启动）
        logger.info("Starting health check server...")
        start_health_check_server(port)
        logger.info("✓ Health check server ready - Cloud Run can now detect the container")
        
        # 导入并启动 Gradio 应用（在后台进行，不阻塞健康检查）
        logger.info("Importing Gradio app module...")
        from app.gradio_app import create_demo
        
        logger.info("Creating Gradio demo interface...")
        demo = create_demo()
        logger.info("✓ Gradio demo created")
        
        logger.info(f"Launching Gradio server on 0.0.0.0:{port}")
        logger.info("Waiting for Gradio to start...")
        
        # 停止健康检查服务器（Gradio 将接管端口）
        if health_server:
            logger.info("Stopping health check server (Gradio will take over)...")
            health_server.shutdown()
            health_server.server_close()
        
        # 启动 Gradio - 使用阻塞模式
        # 重要：server_name 必须是 "0.0.0.0" 才能从外部访问
        # root_path 设置：
        # - 本地开发：不设置或设置为 None（避免 URL 出现双斜杠）
        # - Cloud Run 部署：设置为 "/" 或根据实际路径设置
        root_path = os.getenv("GRADIO_ROOT_PATH", None)
        if root_path == "":
            root_path = None
        
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
        if health_server:
            health_server.shutdown()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        if health_server:
            health_server.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    main()

