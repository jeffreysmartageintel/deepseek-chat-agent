"""
启动脚本：用于 Cloud Run 部署
确保应用正确启动并监听端口
"""
import os
import sys
import logging

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
        
        # 导入并启动 Gradio 应用
        logger.info("Importing Gradio app module...")
        from app.gradio_app import create_demo
        
        logger.info("Creating Gradio demo interface...")
        demo = create_demo()
        logger.info("✓ Gradio demo created")
        
        logger.info(f"Launching Gradio server on 0.0.0.0:{port}")
        logger.info("Waiting for Gradio to start...")
        
        # 启动 Gradio - 使用阻塞模式
        # 重要：server_name 必须是 "0.0.0.0" 才能从外部访问
        demo.launch(
            server_name="0.0.0.0",  # 必须绑定到 0.0.0.0，不能是 127.0.0.1 或 localhost
            server_port=port,
            share=False,
            show_error=True,
            show_api=False,
            prevent_thread_lock=False,  # False = 阻塞模式，保持容器运行
            inbrowser=False,
            root_path="/",
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

