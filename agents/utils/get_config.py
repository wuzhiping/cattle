import os
import uuid
import aiohttp


class Config:
    
    def __init__(self, api_url: str = "https://abc.feg.com.tw/oauth2/worker", token: str = None):
        self.api_url = api_url
        self.token = token or os.getenv("DEVICE_TOKEN")
        self._uuid = uuid.getnode()
    
    async def fetch(self) -> dict:
        """获取配置"""
        async with aiohttp.ClientSession() as s:
            resp = await s.post(self.api_url, json={
                "uuid": self._uuid,
                "token": self.token
            })
            return await resp.json()

