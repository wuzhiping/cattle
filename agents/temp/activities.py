from temporalio import activity

from .ptflow import pocketflow
from .ocagent import OpenCodeAgent

import os
import psutil

@activity.defn(name="OP")
async def OP(payload) -> dict:

    # 输入数据
    # payload = {
    #     "dir": "../demo",
    #     "question": "当前工作目录中的文件"
    # }

    dirt = payload.get("dir")
    qt = payload.get("question")
    
    agent = OpenCodeAgent(directory=dirt)
    output = agent.run_stream(qt)  # 直接是字符串
    
    print(output)  # ✅ 直接打印
    
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
    
    shared =   payload.get("shared",{})
    
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
