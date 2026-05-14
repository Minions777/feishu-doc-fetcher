# 飞书文档获取器

使用Python获取飞书文档的多种实现方式。

## 功能特性

- 🚀 支持多种获取方式：飞书CLI、Python SDK、直接API调用
- 📄 支持获取文档内容、多维表格、电子表格
- 🔄 支持批量获取文档
- 📊 支持导出为多种格式（JSON、Markdown、CSV）

## 安装

### 方式1：使用飞书CLI（推荐）

```bash
# 安装飞书CLI
npm install -g @larksuite/cli

# 安装Python依赖
pip install -r requirements.txt
```

### 方式2：使用Python SDK

```bash
pip install -r requirements.txt
```

## 配置

1. 在飞书开放平台创建应用：https://open.feishu.cn/app
2. 获取App ID和App Secret
3. 配置环境变量或配置文件

### 环境变量配置

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 配置文件

创建 `config.json`：

```json
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret",
  "base_url": "https://open.feishu.cn"
}
```

## 使用方式

### 方式1：使用飞书CLI

```bash
# 获取文档内容
python feishu_cli_fetcher.py --doc-id <document_id>

# 获取多维表格数据
python feishu_cli_fetcher.py --bitable --app-token <app_token> --table-id <table_id>

# 获取电子表格数据
python feishu_cli_fetcher.py --sheet --spreadsheet-token <token> --sheet-id <sheet_id>
```

### 方式2：使用Python SDK

```bash
# 获取文档内容
python feishu_sdk_fetcher.py --doc-id <document_id>

# 获取多维表格数据
python feishu_sdk_fetcher.py --bitable --app-token <app_token> --table-id <table_id>
```

### 方式3：使用直接API调用

```bash
python feishu_api_fetcher.py --doc-id <document_id>
```

## 示例

### 获取文档内容

```python
from feishu_cli_fetcher import FeishuCLIFetcher

# 初始化fetcher
fetcher = FeishuCLIFetcher()

# 获取文档内容
doc_content = fetcher.get_document("doc_id_here")
print(doc_content)
```

### 获取多维表格数据

```python
from feishu_cli_fetcher import FeishuCLIFetcher

fetcher = FeishuCLIFetcher()

# 获取多维表格数据
records = fetcher.get_bitable_records(
    app_token="app_token_here",
    table_id="table_id_here"
)

# 导出为CSV
fetcher.export_to_csv(records, "output.csv")
```

## 项目结构

```
feishu-doc-fetcher/
├── README.md                    # 项目说明
├── requirements.txt             # Python依赖
├── config.json                  # 配置文件示例
├── feishu_cli_fetcher.py        # 飞书CLI方式
├── feishu_sdk_fetcher.py        # Python SDK方式
├── feishu_api_fetcher.py        # 直接API调用方式
├── utils.py                     # 工具函数
└── examples/                    # 示例代码
    ├── get_document.py
    ├── get_bitable.py
    └── get_sheet.py
```

## 注意事项

1. 使用飞书CLI方式需要先安装Node.js和npm
2. 使用Python SDK方式需要安装`larksuiteoapi`包
3. 所有方式都需要在飞书开放平台创建应用并获取凭证
4. 请确保应用有足够的权限访问目标文档

## 许可证

MIT License