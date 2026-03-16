# agent project

## 1.temporal

```
temporal server start-dev --ip 0.0.0.0 
```

安装 Temporal CLI，解压后将 temporal.exe 添加到你的 PATH 环境变量中。

```
wegt https://temporal.download/cli/archive/latest?platform=windows&arch=amd64
```

或 访问 [Temporal Quickstart](https://docs.temporal.io/develop/python/set-up-your-local-python)

---

## 2.下载项目
```
uv sync
```

```
.venv\Scripts\activate
uv run --env-file .env --with jupyter jupyter lab
```

```
.venv\Scripts\activate
uv run --env-file .env worker.py
```
---

## 测试

test.ipynb
