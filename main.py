#!/usr/bin/env python3
"""
Pulsoid to VRChat OSC Bridge - Python版本
将Pulsoid心率数据通过OSC发送到VRChat
"""

import asyncio
import signal
import sys
import logging
from pathlib import Path

# 导入自定义模块
from logger import setup_logging, get_logger
from config import Config
from auth import PulsoidAuth
from websocket_client import PulsoidWebSocketClient
from osc_client import VRChatOSCClient

class PulsoidVRChatBridge:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.auth = PulsoidAuth()
        self.websocket_client = None
        self.osc_client = None
        self.running = False
        
    def setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            self.logger.info("收到中断信号，正在关闭程序...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def on_heart_rate_received(self, heart_rate: int):
        """处理接收到的心率数据"""
        try:
            self.logger.info(f"心率: {heart_rate} bpm")
            
            # 发送到VRChat
            if self.osc_client and self.osc_client.connected:
                success = self.osc_client.send_heart_rate(heart_rate)
                if not success:
                    self.logger.warning("发送心率数据到VRChat失败")
            else:
                self.logger.warning("OSC客户端未连接")
                
        except Exception as e:
            self.logger.error(f"处理心率数据时出错: {e}")
    
    async def initialize(self):
        """初始化所有组件"""
        try:
            self.logger.info("=== Pulsoid to VRChat OSC Bridge (Python版) ===")
            
            # 获取token
            self.logger.info("正在获取认证token...")
            token = self.auth.get_valid_token()
            if not token:
                self.logger.error("无法获取有效的token")
                return False
            
            # 初始化OSC客户端
            self.logger.info("正在初始化OSC客户端...")
            self.osc_client = VRChatOSCClient()
            if not self.osc_client.connect():
                self.logger.error("OSC客户端连接失败")
                return False
            
            # 初始化WebSocket客户端
            self.logger.info("正在初始化WebSocket客户端...")
            self.websocket_client = PulsoidWebSocketClient(
                token=token,
                on_heart_rate=self.on_heart_rate_received
            )
            
            # 发送连接状态
            self.osc_client.send_connection_status(True)
            
            self.logger.info("所有组件初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"初始化失败: {e}")
            return False
    
    async def run(self):
        """运行主程序"""
        try:
            # 初始化
            if not await self.initialize():
                return False
            
            self.running = True
            self.logger.info("程序启动成功，开始接收心率数据...")
            
            # 运行WebSocket客户端
            await self.websocket_client.run_with_reconnect()
            
        except KeyboardInterrupt:
            self.logger.info("收到键盘中断")
        except Exception as e:
            self.logger.error(f"程序运行时出错: {e}")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """优雅关闭程序"""
        if not self.running:
            return
        
        self.running = False
        self.logger.info("正在关闭程序...")
        
        try:
            # 发送断开连接状态
            if self.osc_client and self.osc_client.connected:
                self.osc_client.send_connection_status(False)
            
            # 关闭WebSocket客户端
            if self.websocket_client:
                await self.websocket_client.stop()
            
            # 关闭OSC客户端
            if self.osc_client:
                self.osc_client.disconnect()
            
            self.logger.info("程序已安全关闭")
            
        except Exception as e:
            self.logger.error(f"关闭程序时出错: {e}")

async def main():
    """主函数"""
    # 设置日志
    setup_logging(level=logging.INFO, log_to_file=True)
    logger = get_logger(__name__)
    
    try:
        # 创建并运行桥接程序
        bridge = PulsoidVRChatBridge()
        bridge.setup_signal_handlers()
        await bridge.run()
        
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        # 运行异步主函数
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)