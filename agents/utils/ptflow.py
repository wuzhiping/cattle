from pocketflow import Flow, Node
import time

class SummarizeFile(Node):
    def prep(self, shared):
        # 安全获取数据
        return shared.get("data", "")

    def exec(self, prep_res):
        if not prep_res:
            return "Empty file content"

        time.sleep(0.1)
        
        prompt = f"Summarize this text in 10 words: {prep_res}"
        summary = prompt 
        return summary

    def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
        shared["todos"] = ["A", "B"]
        return None  # 结束流程


def pocketflow(shared, headers=None, ):
    if headers is None:
        headers = {}
    
    summarize_node = SummarizeFile(max_retries=3)
    
    # 正确创建 Flow
    flow = Flow(start=summarize_node)
    
    # run 不需要参数，shared 在 prep 中访问
    flow.run(shared)

    result = {
        "summary": shared.get("summary", "No summary generated"),
        "todos": shared.get("todos", []),
        "original_data": shared.get("data", ""),
        "success": "summary" in shared,
    }
    print(result)
    return result
