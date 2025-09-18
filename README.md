# Pulsoid to VRChat OSC Bridge (Python版)

这是一个用Python重新实现的Pulsoid心率数据到VRChat OSC桥接程序，具有更好的稳定性和错误处理能力。

## 功能特性

- 🔗 **稳定的WebSocket连接**: 支持自动重连和指数退避策略
- 🎮 **VRChat OSC集成**: 将心率数据实时发送到VRChat Avatar参数
- 🔐 **安全的认证管理**: 自动保存和读取Pulsoid认证token
- 📊 **多种心率参数**: 
  - `HeartRate`: 原始心率值 (bpm)
  - `HeartRateNormalized`: 归一化心率值 (0.0-1.0)
  - `HeartRateStatus`: 心率状态 (0=低, 1=正常, 2=高)
  - `PulsoidConnected`: 连接状态
- 🎨 **彩色日志输出**: 清晰的控制台日志显示
- 🔄 **优雅关闭**: 支持Ctrl+C安全退出
- 📝 **详细日志记录**: 支持文件日志记录

## 系统要求

- Python 3.7 或更高版本
- Windows 10/11 或 Linux/macOS
- VRChat (支持OSC)

## 安装和使用

### 方法1: 使用启动脚本 (推荐)

#### Windows:
```bash
# 双击运行或在命令行中执行
run.bat
```

#### Linux/macOS:
```bash
# 给脚本执行权限
chmod +x run.sh

# 运行脚本
./run.sh
```

启动脚本会自动：
- 检查Python环境
- 创建虚拟环境
- 安装依赖包
- 启动程序

### 方法2: 手动安装

1. **克隆或下载项目**
2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```
3. **运行程序**:
   ```bash
   python main.py
   ```

## 首次使用

1. 运行程序后，如果没有保存的token，会自动打开Pulsoid认证页面
2. 在浏览器中登录Pulsoid并授权应用
3. 复制获得的token并粘贴到程序中
4. Token会自动保存到当前目录的 `token.txt` 文件中，下次运行时无需重新输入

## VRChat设置

在VRChat中，你可以使用以下OSC参数：

- `/avatar/parameters/HeartRate` (int): 心率值 (bpm)
- `/avatar/parameters/HeartRateNormalized` (float): 归一化心率 (0.0-1.0)
- `/avatar/parameters/HeartRateStatus` (int): 心率状态 (0=低, 1=正常, 2=高)
- `/avatar/parameters/PulsoidConnected` (bool): 连接状态

## 配置

可以在 `config.py` 中修改以下设置：

- OSC服务器地址和端口
- 重连参数
- 心率范围设置
- 日志级别

## 故障排除

### 常见问题

1. **"无法连接到Pulsoid"**
   - 检查网络连接
   - 确认token是否有效
   - 重新进行认证

2. **"OSC连接失败"**
   - 确认VRChat正在运行
   - 检查OSC端口是否被占用
   - 确认VRChat OSC功能已启用

3. **"依赖包安装失败"**
   - 确认Python版本 >= 3.7
   - 尝试升级pip: `python -m pip install --upgrade pip`
   - 使用虚拟环境

### 日志文件

程序会在运行目录生成 `pulsoid_vrchat.log` 日志文件，包含详细的运行信息。

## 项目结构

```
pulsoid-to-vrchat-python/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── auth.py              # 认证模块
├── websocket_client.py  # WebSocket客户端
├── osc_client.py        # OSC客户端
├── logger.py            # 日志配置
├── requirements.txt     # Python依赖
├── run.bat             # Windows启动脚本
├── run.sh              # Linux/macOS启动脚本
└── README.md           # 说明文档
```

## 与Node.js版本的区别

- ✅ 更好的错误处理和恢复机制
- ✅ 彩色日志输出
- ✅ 自动虚拟环境管理
- ✅ 跨平台启动脚本
- ✅ 更清晰的代码结构
- ✅ 详细的文档说明

## 许可证

本项目基于原Node.js版本重新实现，保持相同的功能和兼容性。