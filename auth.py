import os
import webbrowser
from pathlib import Path
from config import Config
import logging

logger = logging.getLogger(__name__)

class PulsoidAuth:
    def __init__(self):
        self.token_path = self._get_token_path()
    
    def _get_token_path(self):
        """确定token文件路径 - 始终在当前程序目录下"""
        # 获取当前脚本所在目录
        script_dir = Path(__file__).parent
        return script_dir / Config.TOKEN_FILE
    
    def read_token(self):
        """读取保存的token"""
        try:
            if self.token_path.exists():
                with open(self.token_path, 'r', encoding='utf-8') as f:
                    token = f.read().strip()
                    if token:
                        logger.info("成功读取已保存的token")
                        return token
            return None
        except Exception as e:
            logger.error(f"读取token文件失败: {e}")
            return None
    
    def save_token(self, token):
        """保存token到文件"""
        try:
            # 确保目录存在
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.token_path, 'w', encoding='utf-8') as f:
                f.write(token)
            logger.info(f"Token已保存到: {self.token_path}")
            return True
        except Exception as e:
            logger.error(f"保存token失败: {e}")
            return False
    
    def start_auth(self):
        """开始认证流程"""
        print("\n=== Pulsoid 认证 ===")
        print("正在打开认证页面...")
        
        auth_url = Config.get_auth_url()
        try:
            webbrowser.open(auth_url)
            print(f"认证URL: {auth_url}")
        except Exception as e:
            logger.error(f"无法打开浏览器: {e}")
            print(f"请手动打开以下URL进行认证:")
            print(auth_url)
        
        print("\n请在浏览器中完成认证，然后复制获得的token")
        print("Token格式类似: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        
        while True:
            token = input("\n请输入Auth Token: ").strip()
            if token:
                if self.save_token(token):
                    print("Token保存成功!")
                    return token
                else:
                    print("Token保存失败，请重试")
            else:
                print("Token不能为空，请重新输入")
    
    def get_valid_token(self):
        """获取有效的token，如果没有则启动认证流程"""
        token = self.read_token()
        if not token:
            print("无token，开始认证流程...")
            token = self.start_auth()
        return token