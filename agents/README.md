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
uv run --env-file .env --with jupyter jupyter lab
```

```
uv run --env-file .env worker.py
```
---

## 3.测试

查看test.ipynb

---

## 4.NSSM

### NSSM是一个服务封装程序，它可以将普通exe程序封装成服务，使之像windows服务一样运行。

下载地址：[https://nssm.cc/download](https://nssm.cc/download)
具体文件：[https://nssm.cc/release/nssm-2.24.zip](https://nssm.cc/release/nssm-2.24.zip)

### 以管理员运行 PowerShell，打开NSSM的win64的文件夹，可执行以下命令：
- 安装服务
```
nssm install [service name]
```
调出设置窗体:
- Path: 可执行文件完整路径
- Startup directory: 工作目录（程序运行时的当前目录）
- Arguments: 传递给程序的参数

设置完成后点击Install service按钮即完成，此时去查看系统服务有多了这个服务了

例如 把“uv run --env-file .env worker.py”封装成服务
```
Path: ...（你的目录）\uv.exe
Startup directory: uv项目文件地址
Arguments: run --env-file .env worker.py
```

- 启动服务
```
nssm start [service name]
```

- 停止服务
```
nssm stop [service name]
```

- 删除服务
```
nssm remove [service name]
```

- 删除服务确定
```
nssm remove [service name] confirm  
```

- 编辑服务
```
nssm edit [service name]
```



