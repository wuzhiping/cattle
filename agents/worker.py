import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from temp.workflows import OPflow, PTflow, AuditFlow
from temp.activities import OP, PT, Audit
import aiohttp
import uuid
import os

async def fetch_config():
    device = uuid.getnode()
    token = os.getenv("DEVICE_TOKEN")
    
    # print("device:", device)
    # print("token:", token)
    
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            "https://abc.feg.com.tw/oauth2/worker",
            json = {
                device: device,
                token: token
            })
        return await resp.json()


async def worker():
    config = await fetch_config()
    
    api_temporal = config.get("temporal", {})
    if not api_temporal:
        print("temporal is empty !")
        return
        
    api_address = api_temporal.get("addr", "10.17.1.12:7233")
    api_namespace = api_temporal.get("namespace", "default")
    api_task_queue = api_temporal.get("task_queue", "_device_")

    # print(api_temporal)
    # print(api_address)
    # print(api_namespace)
    # print(api_task_queue)
    
    client = await Client.connect(api_address, namespace=api_namespace)

    worker = Worker(
        client,
        task_queue=api_task_queue,
        workflows=[OPflow, PTflow, AuditFlow],
        activities=[OP, PT, Audit]
    )
    print("worker started")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(worker())
