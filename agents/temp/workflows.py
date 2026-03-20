from datetime import timedelta
from temporalio import workflow


@workflow.defn
class OPflow:
    @workflow.run
    async def run(self, payload: str) -> dict:
        data = await workflow.execute_activity(
            "OP",
            payload,
            start_to_close_timeout=timedelta(seconds=60),
        )
        return data

@workflow.defn
class PTflow:
    @workflow.run
    async def run(self, payload: str) -> dict:
        data = await workflow.execute_activity(
            "PT",
            payload,
            start_to_close_timeout=timedelta(seconds=60),
        )
        return data


@workflow.defn
class AuditFlow:
    @workflow.run
    async def run(self, payload: str) -> dict:
        data = await workflow.execute_activity(
            "Audit",
            payload,
            start_to_close_timeout=timedelta(seconds=60),
        )
        return data