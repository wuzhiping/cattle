import subprocess
import threading
import platform
import shutil


class OpenCodeAgent:

    def __init__(
        self,
        model="opencode/big-pickle",
        agent="build",
        directory=".",
        thinking=True,
    ):
        self.model = model
        self.agent = agent
        self.directory = directory
        self.thinking = thinking
        self._opencode_cmd = self._find_opencode()

    def _find_opencode(self):
        """查找 opencode 可执行文件路径"""
        # 1. 首先尝试直接找到 opencode 命令
        opencode_path = shutil.which("opencode")
        if opencode_path:
            return opencode_path
        
        # 2. Windows 下尝试常见安装位置
        if platform.system() == "Windows":
            import os
            # 尝试 npm 全局安装路径
            try:
                npm_prefix = subprocess.run(
                    ["npm", "config", "get", "prefix"],
                    capture_output=True, text=True, shell=True
                ).stdout.strip()
                
                possible_paths = [
                    os.path.join(npm_prefix, "opencode.cmd"),
                    os.path.join(npm_prefix, "node_modules", ".bin", "opencode.cmd"),
                    os.path.expandvars(r"%APPDATA%\npm\opencode.cmd"),
                    r"C:\Program Files\nodejs\opencode.cmd",
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        return path
            except Exception:
                pass
        
        # 3. 如果都找不到，返回 "opencode" 让系统尝试解析
        return "opencode"

    def _build_cmd(self, task):
        cmd = [
            self._opencode_cmd,
            "run",
            task,
            "-m",
            self.model,
            "--agent",
            self.agent,
            "--dir",
            self.directory,
        ]

        if self.thinking:
            cmd.append("--thinking")

        return cmd

    def _get_subprocess_kwargs(self):
        """获取适用于当前平台的 subprocess 参数"""
        kwargs = {
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace"
        }
        
        if platform.system() == "Windows":
            # Windows 需要 shell=True 来正确解析 .cmd 文件
            kwargs["shell"] = True
        
        return kwargs

    def run(self, task):
        """同步执行"""
        cmd = self._build_cmd(task)
        kwargs = self._get_subprocess_kwargs()

        result = subprocess.run(cmd, **kwargs)

        return {
            "task": task,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }

    def run_stream(self, task):
        """流式执行"""
        cmd = self._build_cmd(task)
        
        kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "bufsize": 1,
            "universal_newlines": True
        }
        
        if platform.system() == "Windows":
            kwargs["shell"] = True

        process = subprocess.Popen(cmd, **kwargs)

        output = []

        for line in process.stdout:
            print(line, end="", flush=True)
            output.append(line)

        process.wait()

        return "".join(output)

    def batch(self, tasks):
        """批量执行"""
        results = []

        for t in tasks:
            print(f"\n===== TASK: {t} =====")
            res = self.run_stream(t)
            results.append(res)

        return results

    def parallel(self, tasks):
        """并行执行"""
        threads = []

        for task in tasks:
            t = threading.Thread(
                target=self.run_stream,
                args=(task,)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()