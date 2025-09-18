import base64
import uuid

class Config:
    # Pulsoid API配置
    PULSOID_BASE_URL = "https://pulsoid.net/oauth2/authorize"
    PULSOID_CLIENT_ID = base64.b64decode("ZGZhY2U5Y2EtMGZjYi00YjMxLTg4NzQtZGQ0YWRhZGJiYjA3").decode()
    PULSOID_REDIRECT_URI = ""
    PULSOID_RESPONSE_TYPE = "token"
    PULSOID_SCOPE = "data:heart_rate:read"
    PULSOID_RESPONSE_MODE = "web_page"
    
    # WebSocket配置
    WEBSOCKET_URL = "wss://dev.pulsoid.net/api/v1/data/real_time"
    
    # OSC配置
    OSC_IP = "127.0.0.1"
    OSC_PORT = 9000
    
    # 重连配置
    MAX_RECONNECT_ATTEMPTS = 5
    INITIAL_RECONNECT_DELAY = 1
    MAX_RECONNECT_DELAY = 30
    
    # 文件路径
    TOKEN_FILE = "token.txt"
    
    @staticmethod
    def get_uuid(short=False):
        """生成UUID"""
        uid = str(uuid.uuid4())
        return uid.replace('-', '') if short else uid
    
    @staticmethod
    def get_auth_url():
        """获取认证URL"""
        state = Config.get_uuid(True)
        return (f"{Config.PULSOID_BASE_URL}?"
                f"client_id={Config.PULSOID_CLIENT_ID}&"
                f"redirect_uri={Config.PULSOID_REDIRECT_URI}&"
                f"response_type={Config.PULSOID_RESPONSE_TYPE}&"
                f"scope={Config.PULSOID_SCOPE}&"
                f"state={state}&"
                f"response_mode={Config.PULSOID_RESPONSE_MODE}")