import logging
import sys
from datetime import datetime
from colorama import init, Fore, Back, Style

# 初始化colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
    }
    
    def format(self, record):
        # 获取颜色
        color = self.COLORS.get(record.levelname, '')
        
        # 格式化时间
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # 构建日志消息
        if record.levelname in ['ERROR', 'CRITICAL']:
            # 错误日志显示更多信息
            log_message = f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{Style.RESET_ALL}"
            if record.exc_info:
                log_message += f"\n{self.formatException(record.exc_info)}"
        else:
            log_message = f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{Style.RESET_ALL}"
        
        return log_message

def setup_logging(level=logging.INFO, log_to_file=False):
    """设置日志配置"""
    
    # 创建根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    if log_to_file:
        file_handler = logging.FileHandler('pulsoid_vrchat.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger('websockets').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name):
    """获取指定名称的日志器"""
    return logging.getLogger(name)