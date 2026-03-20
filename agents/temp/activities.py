from temporalio import activity

from utils.ptflow import pocketflow
from utils.oc_agent import OpenCodeAgent
from utils.get_config import Config
from utils.blowfish_ctr import decrypt

import os
import json
import time
import psutil

# 解密和验证
async def _decrypt_and_verify(encrypted: str, max_gap: int = 180) -> dict:
    try:
        # 获取key
        config = await Config().fetch()
        _key = config.get("temporal").get("task_queue")
        
        # 解密
        plaintext = decrypt(str(_key), encrypted)
        
    except Exception as e:
        raise CryptoError(f"解密失败: {e}")

    # 分割字符串
    if "at" not in plaintext:
        raise ValueError("格式错误：缺少 'at' 分隔符")
    
    # 从末尾找最后一个 "at"（防止 JSON 内容中也有 "at"）
    json_str, timestamp_str = plaintext.rsplit("at", 1)
    
    # 解析时间戳
    stored_timestamp = int(timestamp_str)
    
    # 获取当前时间
    current_timestamp = int(time.time())
    # print("activity current time", current_timestamp)

    # 绝对值间隔
    gap = abs(current_timestamp - stored_timestamp)  
    # print(f"间隔: {gap}秒")
    
    # 判断是否超时
    if gap > max_gap:
        raise RuntimeError(f"时间戳间隔过大！间隔 {gap} 秒，超过最大允许 {max_gap} 秒")
    
    # 解析原始数据
    data = json.loads(json_str)

    return data


@activity.defn(name="OP")
async def OP(payload) -> dict:

    # 输入数据
    # payload = {
    #     "dir": "../demo",
    #     "question": "当前工作目录中的文件"
    # }

    dec = await _decrypt_and_verify(payload)
    dirt = dec.get("dir")
    qt = dec.get("question")
    
    agent = OpenCodeAgent(directory=dirt)
    output = agent.run_stream(qt) 
    
    print(output) 
    
    return {
        "stdout": output,
        "stderr": "",
        "code": 0
    }



@activity.defn(name="PT")
async def PT(payload) -> dict:

    # 输入数据
    # payload = {
    #     "shared": {
    #         "data": "这是一段需要总结的文本..."
    #     }
    # }
    
    dec = await _decrypt_and_verify(payload)
    shared =   dec.get("shared",{})
    
    try:
        result = pocketflow(shared) 
        return result
        
    except Exception as e:
        raise 
    


@activity.defn(name="Audit")
async def Audit(payload) -> dict:

    # 输入数据
    # payload = {
    #     "data": "查看CPU，内存，磁盘使用情况..."
    # }
    
    # 内存
    mem = psutil.virtual_memory()
    # 磁盘
    disk = psutil.disk_usage('/')

    return {
        "cpu": f"CPU: {psutil.cpu_percent()}% ({psutil.cpu_count()}核)",
        "memory": f"内存: {mem.percent}%",
        "disk": f"磁盘: {disk.percent}%"
    }
