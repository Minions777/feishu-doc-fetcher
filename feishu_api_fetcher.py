#!/usr/bin/env python3
"""
飞书API方式获取文档

直接调用飞书开放平台API获取文档内容
"""

import json
import os
import sys
from typing import Dict, List, Optional, Any

import requests
from loguru import logger


class FeishuAPIFetcher:
    """
    使用飞书API获取文档的类
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化飞书API Fetcher
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.base_url = self.config.get("base_url", "https://open.feishu.cn")
        self.tenant_access_token = None
        
        # 获取access token
        if self.config.get("app_id") and self.config.get("app_secret"):
            self.tenant_access_token = self._get_tenant_access_token()
    
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
    
    def _get_tenant_access_token(self) -> str:
        """
        获取tenant_access_token
        
        Returns:
            tenant_access_token
        """
        url = f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config["app_id"],
            "app_secret": self.config["app_secret"]
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                token = data.get("tenant_access_token")
                logger.info("成功获取tenant_access_token")
                return token
            else:
                logger.error(f"获取token失败: {data.get('msg')}")
                return None
                
        except Exception as e:
            logger.error(f"获取token异常: {e}")
            return None
    
    def _get_headers(self) -> Dict[str, str]:
        """
        获取请求头
        
        Returns:
            请求头字典
        """
        return {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        获取飞书文档内容
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档内容
        """
        url = f"{self.base_url}/open-apis/docx/v1/documents/{doc_id}/raw_content"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取文档失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取文档异常: {e}")
            return {"error": str(e)}
    
    def get_document_blocks(self, doc_id: str) -> Dict[str, Any]:
        """
        获取文档块信息
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档块信息
        """
        url = f"{self.base_url}/open-apis/docx/v1/documents/{doc_id}/blocks"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取文档块失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取文档块异常: {e}")
            return {"error": str(e)}
    
    def get_bitable_meta(self, app_token: str) -> Dict[str, Any]:
        """
        获取多维表格元数据
        
        Args:
            app_token: 多维表格app_token
            
        Returns:
            元数据信息
        """
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{app_token}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取元数据失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取元数据异常: {e}")
            return {"error": str(e)}
    
    def get_bitable_tables(self, app_token: str) -> Dict[str, Any]:
        """
        获取多维表格中的表格列表
        
        Args:
            app_token: 多维表格app_token
            
        Returns:
            表格列表
        """
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{app_token}/tables"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取表格列表失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取表格列表异常: {e}")
            return {"error": str(e)}
    
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
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        
        params = {
            "page_size": page_size
        }
        
        if page_token:
            params["page_token"] = page_token
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取记录失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取记录异常: {e}")
            return {"error": str(e)}
    
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
            records = result.get("items", [])
            all_records.extend(records)
            
            # 检查是否有下一页
            has_more = result.get("has_more", False)
            page_token = result.get("page_token")
            
            if not has_more or not page_token:
                break
            
            logger.info(f"已获取 {len(all_records)} 条记录，继续获取下一页...")
        
        logger.info(f"总共获取 {len(all_records)} 条记录")
        return all_records
    
    def get_sheet_meta(
        self, 
        spreadsheet_token: str
    ) -> Dict[str, Any]:
        """
        获取电子表格元数据
        
        Args:
            spreadsheet_token: 电子表格token
            
        Returns:
            元数据信息
        """
        url = f"{self.base_url}/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取元数据失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取元数据异常: {e}")
            return {"error": str(e)}
    
    def get_sheet_values(
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
        if range_str:
            range_param = f"{sheet_id}!{range_str}"
        else:
            range_param = sheet_id
        
        url = f"{self.base_url}/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{range_param}"
        
        params = {
            "valueRenderOption": "ToString",
            "dateTimeRenderOption": "FormattedString"
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"获取数据失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"获取数据异常: {e}")
            return {"error": str(e)}
    
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
        url = f"{self.base_url}/open-apis/suite/docs-api/search/object"
        
        payload = {
            "search_key": query,
            "count": count,
            "offset": 0,
            "owner_ids": [],
            "docs_types": []
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {})
            else:
                logger.error(f"搜索失败: {data.get('msg')}")
                return {"error": data.get("msg")}
                
        except Exception as e:
            logger.error(f"搜索异常: {e}")
            return {"error": str(e)}
    
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
    
    parser = argparse.ArgumentParser(description="飞书API文档获取器")
    parser.add_argument("--doc-id", help="文档ID")
    parser.add_argument("--bitable", action="store_true", help="获取多维表格数据")
    parser.add_argument("--app-token", help="多维表格app_token")
    parser.add_argument("--table-id", help="表格ID")
    parser.add_argument("--sheet", action="store_true", help="获取电子表格数据")
    parser.add_argument("--spreadsheet-token", help="电子表格token")
    parser.add_argument("--sheet-id", help="工作表ID")
    parser.add_argument("--search", help="搜索文档")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 初始化fetcher
    fetcher = FeishuAPIFetcher()
    
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
            fetcher.export_to_json(records, args.output)
        else:
            print(json.dumps(records, ensure_ascii=False, indent=2))
            
    elif args.sheet and args.spreadsheet_token and args.sheet_id:
        data = fetcher.get_sheet_values(args.spreadsheet_token, args.sheet_id)
        if args.output:
            fetcher.export_to_json(data, args.output)
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()