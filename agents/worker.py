import asyncio
from temporalio.worker import Worker
from temporalio.client import Client

from temp.workflows import OPflow, PTflow, AuditFlow
from temp.activities import OP, PT, Audit
from utils.get_config import Config


async def worker():
    # 获取配置
    config = await Config(token="123456").fetch()
    # print(config)
    
    _t = config.get("temporal")
    _addr, _ns, _queue ,_rpc_metadata= _t.get("addr"), _t.get("namespace"), _t.get("task_queue"),_t.get("rpc_metadata")
    
    if None in (_addr, _ns, _queue):
        raise ValueError(f"missing required: addr={_addr}, ns={_ns}, queue={_queue}")
    queue = str(_queue)  

    # worker
    client = await Client.connect(_addr, namespace=_ns,rpc_metadata=_rpc_metadata)

    worker = Worker(
        client,
        task_queue=queue,
        workflows=[OPflow, PTflow, AuditFlow],
        activities=[OP, PT, Audit]
    )
    print("worker started")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(worker())
