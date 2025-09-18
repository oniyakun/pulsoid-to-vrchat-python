import logging
from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
from config import Config
import threading
import time

logger = logging.getLogger(__name__)

class VRChatOSCClient:
    def __init__(self):
        self.client = None
        self.connected = False
        self.last_heart_rate = 0
        self.keepalive_thread = None
        self.running = False
        self.hb_toggle = False  # 心跳切换状态
        
    def connect(self):
        """连接到VRChat OSC"""
        try:
            self.client = udp_client.SimpleUDPClient(Config.OSC_IP, Config.OSC_PORT)
            self.connected = True
            self.running = True
            logger.info(f"OSC客户端已连接到 {Config.OSC_IP}:{Config.OSC_PORT}")
            
            # 启动保活线程
            self.start_keepalive()
            return True
            
        except Exception as e:
            logger.error(f"OSC连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开OSC连接"""
        self.running = False
        self.connected = False
        
        if self.keepalive_thread and self.keepalive_thread.is_alive():
            self.keepalive_thread.join(timeout=1)
        
        logger.info("OSC客户端已断开")
    
    def send_heart_rate(self, heart_rate: int):
        """发送心率数据到VRChat - 完全匹配Node.js版本的参数"""
        if not self.connected or not self.client:
            logger.warning("OSC未连接，无法发送心率数据")
            return False
        
        try:
            # 参考自该代码：
            # https://github.com/vard88508/vrc-osc-miband-hrm/blob/f60c3422c36921d317168ed38b1362528e8364e9/app.js#L24-L50
            # 完全匹配Node.js版本的心率参数
            heartrates = [
                {
                    'address': '/avatar/parameters/Heartrate',
                    'args': {
                        'type': 'f',
                        'value': heart_rate / 127 - 1
                    }
                },
                {
                    'address': "/avatar/parameters/HeartRateFloat",
                    'args': {
                        'type': "f",
                        'value': heart_rate / 127 - 1
                    }
                },
                {
                    'address': "/avatar/parameters/Heartrate2",
                    'args': {
                        'type': "f",
                        'value': heart_rate / 255
                    }
                },
                {
                    'address': "/avatar/parameters/HeartRateFloat01",
                    'args': {
                        'type': "f",
                        'value': heart_rate / 255
                    }
                },
                {
                    'address': "/avatar/parameters/Heartrate3",
                    'args': {
                        'type': "i",
                        'value': heart_rate
                    }
                },
                {
                    'address': "/avatar/parameters/HeartRateInt",
                    'args': {
                        'type': "i",
                        'value': heart_rate
                    }
                },
                {
                    'address': "/avatar/parameters/HeartBeatToggle",
                    'args': {
                        'type': "b",
                        'value': self.hb_toggle
                    }
                }
            ]
            
            # 发送所有心率参数
            for element in heartrates:
                try:
                    address = element['address']
                    value = element['args']['value']
                    
                    self.client.send_message(address, value)
                    
                    # 心跳切换参数发送后切换状态
                    if address == "/avatar/parameters/HeartBeatToggle":
                        self.hb_toggle = not self.hb_toggle
                        
                except Exception as e:
                    logger.error(f"发送OSC消息失败 {element['address']}: {e}")
            
            self.last_heart_rate = heart_rate
            logger.debug(f"已发送心率数据到VRChat: {heart_rate} bpm")
            return True
            
        except Exception as e:
            logger.error(f"发送OSC消息失败: {e}")
            return False
    
    def send_keepalive(self):
        """发送保活消息"""
        if not self.connected or not self.client:
            return
        
        try:
            # 发送保活信号
            self.client.send_message("/avatar/parameters/PulsoidConnected", True)
            logger.debug("已发送OSC保活信号")
        except Exception as e:
            logger.warning(f"发送保活信号失败: {e}")
    
    def start_keepalive(self):
        """启动保活线程"""
        def keepalive_worker():
            while self.running:
                self.send_keepalive()
                time.sleep(30)  # 每30秒发送一次保活信号
        
        self.keepalive_thread = threading.Thread(target=keepalive_worker, daemon=True)
        self.keepalive_thread.start()
        logger.info("OSC保活线程已启动")
    
    def send_connection_status(self, connected: bool):
        """发送连接状态"""
        if not self.connected or not self.client:
            return
        
        try:
            self.client.send_message("/avatar/parameters/PulsoidConnected", connected)
            logger.debug(f"已发送连接状态: {connected}")
        except Exception as e:
            logger.warning(f"发送连接状态失败: {e}")
    
    def send_custom_parameter(self, parameter: str, value):
        """发送自定义参数"""
        if not self.connected or not self.client:
            logger.warning("OSC未连接，无法发送自定义参数")
            return False
        
        try:
            self.client.send_message(f"/avatar/parameters/{parameter}", value)
            logger.debug(f"已发送自定义参数: {parameter} = {value}")
            return True
        except Exception as e:
            logger.error(f"发送自定义参数失败: {e}")
            return False