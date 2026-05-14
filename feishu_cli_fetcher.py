#!/usr/bin/env python3
"""
飞书CLI方式获取文档

使用飞书官方CLI工具获取文档内容
"""

import subprocess
import json
import os
import sys
from typing import Dict, List, Optional, Any
from pathlib import Path

import pandas as pd
from loguru import logger


class FeishuCLIFetcher:
    """
    使用飞书CLI获取文档的类
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化飞书CLI Fetcher
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self._check_cli_installed()
        
    def _load_config(self, config_path: str) -> Dict[str, str]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        # 首先尝试从环境变量获取
        app_id = os.getenv("FEISHU_APP_ID")
        app_secret = os.getenv("FEISHU_APP_SECRET")
        
        if app_id and app_secret:
            return {
                "app_id": app_id,
                "app_secret": app_secret
            }
        
        # 尝试从配置文件获取
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 如果都没有，提示用户配置
        logger.warning("未找到配置，请先配置飞书应用凭证")
        logger.info("可以通过以下方式配置：")
        logger.info("1. 设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        logger.info("2. 创建 config.json 文件")
        return {}
    
    def _check_cli_installed(self):
        """
        检查飞书CLI是否已安装
        """
        try:
            result = subprocess.run(
                ["lark-cli", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"飞书CLI版本: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("飞书CLI未安装，请先安装: npm install -g @larksuite/cli")
            sys.exit(1)
    
    def _run_cli_command(self, command: List[str]) -> Dict[str, Any]:
        """
        执行CLI命令
        
        Args:
            command: CLI命令列表
            
        Returns:
            命令输出的JSON数据
        """
        try:
            logger.info(f"执行命令: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            
            # 尝试解析JSON输出
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"output": result.stdout}
                
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e.stderr}")
            return {"error": e.stderr}
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        获取飞书文档内容
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档内容
        """
        command = [
            "lark-cli", "docs", "+read",
            "--document-id", doc_id,
            "--output", "json"
        ]
        
        return self._run_cli_command(command)
    
    def get_bitable_records(
        self, 
        app_token: str, 
        table_id: str,
        page_size: int = 100,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取多维表格记录
        
        Args:
            app_token: 多维表格app_token
            table_id: 表格ID
            page_size: 每页记录数
            page_token: 分页token
            
        Returns:
            表格记录数据
        """
        command = [
            "lark-cli", "base", "+list-records",
            "--app-token", app_token,
            "--table-id", table_id,
            "--page-size", str(page_size),
            "--output", "json"
        ]
        
        if page_token:
            command.extend(["--page-token", page_token])
        
        return self._run_cli_command(command)
    
    def get_all_bitable_records(
        self, 
        app_token: str, 
        table_id: str
    ) -> List[Dict[str, Any]]:
        """
        获取多维表格所有记录（自动分页）
        
        Args:
            app_token: 多维表格app_token
            table_id: 表格ID
            
        Returns:
            所有记录列表
        """
        all_records = []
        page_token = None
        
        while True:
            result = self.get_bitable_records(
                app_token=app_token,
                table_id=table_id,
                page_size=500,
                page_token=page_token
            )
            
            if "error" in result:
                logger.error(f"获取记录失败: {result['error']}")
                break
            
            # 提取记录
            records = result.get("data", {}).get("items", [])
            all_records.extend(records)
            
            # 检查是否有下一页
            has_more = result.get("data", {}).get("has_more", False)
            page_token = result.get("data", {}).get("page_token")
            
            if not has_more or not page_token:
                break
            
            logger.info(f"已获取 {len(all_records)} 条记录，继续获取下一页...")
        
        logger.info(f"总共获取 {len(all_records)} 条记录")
        return all_records
    
    def get_sheet_data(
        self, 
        spreadsheet_token: str, 
        sheet_id: str,
        range_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取电子表格数据
        
        Args:
            spreadsheet_token: 电子表格token
            sheet_id: 工作表ID
            range_str: 单元格范围（如 A1:D10）
            
        Returns:
            表格数据
        """
        command = [
            "lark-cli", "sheets", "+read",
            "--spreadsheet-token", spreadsheet_token,
            "--sheet-id", sheet_id,
            "--output", "json"
        ]
        
        if range_str:
            command.extend(["--range", range_str])
        
        return self._run_cli_command(command)
    
    def search_documents(
        self, 
        query: str, 
        count: int = 20
    ) -> Dict[str, Any]:
        """
        搜索飞书文档
        
        Args:
            query: 搜索关键词
            count: 返回结果数量
            
        Returns:
            搜索结果
        """
        command = [
            "lark-cli", "drive", "+search",
            "--query", query,
            "--count", str(count),
            "--output", "json"
        ]
        
        return self._run_cli_command(command)
    
    def export_to_csv(
        self, 
        records: List[Dict[str, Any]], 
        output_path: str
    ):
        """
        将记录导出为CSV文件
        
        Args:
            records: 记录列表
            output_path: 输出文件路径
        """
        if not records:
            logger.warning("没有记录可导出")
            return
        
        # 提取字段
        fields = set()
        for record in records:
            fields.update(record.get("fields", {}).keys())
        
        # 转换为DataFrame
        data = []
        for record in records:
            row = {"record_id": record.get("record_id", "")}
            fields_data = record.get("fields", {})
            for field in fields:
                value = fields_data.get(field, "")
                # 处理复杂类型
                if isinstance(value, list):
                    value = json.dumps(value, ensure_ascii=False)
                elif isinstance(value, dict):
                    value = json.dumps(value, ensure_ascii=False)
                row[field] = value
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"已导出 {len(records)} 条记录到 {output_path}")
    
    def export_to_json(
        self, 
        data: Any, 
        output_path: str
    ):
        """
        将数据导出为JSON文件
        
        Args:
            data: 要导出的数据
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"已导出数据到 {output_path}")


def main():
    """
    主函数 - 命令行接口
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书CLI文档获取器")
    parser.add_argument("--doc-id", help="文档ID")
    parser.add_argument("--bitable", action="store_true", help="获取多维表格数据")
    parser.add_argument("--app-token", help="多维表格app_token")
    parser.add_argument("--table-id", help="表格ID")
    parser.add_argument("--sheet", action="store_true", help="获取电子表格数据")
    parser.add_argument("--spreadsheet-token", help="电子表格token")
    parser.add_argument("--sheet-id", help="工作表ID")
    parser.add_argument("--search", help="搜索文档")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    # 初始化fetcher
    fetcher = FeishuCLIFetcher()
    
    # 根据参数执行相应操作
    if args.search:
        results = fetcher.search_documents(args.search)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
    elif args.doc_id:
        doc = fetcher.get_document(args.doc_id)
        if args.output:
            fetcher.export_to_json(doc, args.output)
        else:
            print(json.dumps(doc, ensure_ascii=False, indent=2))
            
    elif args.bitable and args.app_token and args.table_id:
        records = fetcher.get_all_bitable_records(args.app_token, args.table_id)
        if args.output:
            if args.format == "csv":
                fetcher.export_to_csv(records, args.output)
            else:
                fetcher.export_to_json(records, args.output)
        else:
            print(json.dumps(records, ensure_ascii=False, indent=2))
            
    elif args.sheet and args.spreadsheet_token and args.sheet_id:
        data = fetcher.get_sheet_data(args.spreadsheet_token, args.sheet_id)
        if args.output:
            fetcher.export_to_json(data, args.output)
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()