import asyncio
import websockets
import json
import logging
from typing import Callable, Optional
from config import Config

logger = logging.getLogger(__name__)

class PulsoidWebSocketClient:
    def __init__(self, token: str, on_heart_rate: Callable[[int], None]):
        self.token = token
        self.on_heart_rate = on_heart_rate
        self.websocket = None
        self.running = False
        self.reconnect_attempts = 0
        self.reconnect_delay = Config.INITIAL_RECONNECT_DELAY
        
    async def connect(self):
        """连接到Pulsoid WebSocket"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            
            logger.info(f"正在连接到 {Config.WEBSOCKET_URL}")
            self.websocket = await websockets.connect(
                Config.WEBSOCKET_URL,
                extra_headers=headers,
                ping_interval=30,
                ping_timeout=10
            )
            
            logger.info("WebSocket连接成功")
            self.reconnect_attempts = 0
            self.reconnect_delay = Config.INITIAL_RECONNECT_DELAY
            return True
            
        except Exception as e:
            logger.error(f"WebSocket连接失败: {e}")
            return False
    
    async def listen(self):
        """监听WebSocket消息"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    if 'measured_at' in data and 'data' in data:
                        heart_rate = data['data'].get('heart_rate')
                        if heart_rate is not None:
                            logger.debug(f"收到心率数据: {heart_rate} bpm")
                            self.on_heart_rate(heart_rate)
                    else:
                        logger.debug(f"收到其他消息: {data}")
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON解析失败: {e}")
                except Exception as e:
                    logger.error(f"处理消息时出错: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket连接已关闭")
        except Exception as e:
            logger.error(f"监听WebSocket时出错: {e}")
    
    async def disconnect(self):
        """断开WebSocket连接"""
        self.running = False
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("WebSocket连接已关闭")
            except Exception as e:
                logger.error(f"关闭WebSocket时出错: {e}")
    
    async def run_with_reconnect(self):
        """运行WebSocket客户端，支持自动重连"""
        self.running = True
        
        while self.running:
            try:
                # 尝试连接
                if await self.connect():
                    # 连接成功，开始监听
                    await self.listen()
                
                # 如果到这里说明连接断开了
                if not self.running:
                    break
                
                # 检查是否需要重连
                if self.reconnect_attempts < Config.MAX_RECONNECT_ATTEMPTS:
                    self.reconnect_attempts += 1
                    logger.info(f"准备重连 (尝试 {self.reconnect_attempts}/{Config.MAX_RECONNECT_ATTEMPTS})")
                    logger.info(f"等待 {self.reconnect_delay} 秒后重连...")
                    
                    await asyncio.sleep(self.reconnect_delay)
                    
                    # 指数退避
                    self.reconnect_delay = min(
                        self.reconnect_delay * 2, 
                        Config.MAX_RECONNECT_DELAY
                    )
                else:
                    logger.error("达到最大重连次数，停止重连")
                    break
                    
            except KeyboardInterrupt:
                logger.info("收到中断信号，正在关闭...")
                break
            except Exception as e:
                logger.error(f"WebSocket运行时出错: {e}")
                if self.running:
                    await asyncio.sleep(self.reconnect_delay)
        
        await self.disconnect()
    
    async def stop(self):
        """停止WebSocket客户端"""
        logger.info("正在停止WebSocket客户端...")
        await self.disconnect()