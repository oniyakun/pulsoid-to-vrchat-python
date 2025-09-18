#!/bin/bash

echo "========================================"
echo " Pulsoid to VRChat OSC Bridge (Python)"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "错误: 未找到main.py文件"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
fi

echo "正在激活虚拟环境..."
source venv/bin/activate

echo "正在安装/更新依赖包..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "警告: 依赖包安装可能有问题，但继续运行..."
fi

echo
echo "正在启动程序..."
echo "按 Ctrl+C 可以停止程序"
echo

# 运行主程序
python main.py

echo
echo "程序已退出"