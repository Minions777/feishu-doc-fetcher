#!/usr/bin/env python3
"""
获取飞书文档示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_cli_fetcher import FeishuCLIFetcher
from feishu_api_fetcher import FeishuAPIFetcher


def example_cli():
    """
    使用CLI方式获取文档
    """
    print("=== 使用飞书CLI获取文档 ===")
    
    # 初始化fetcher
    fetcher = FeishuCLIFetcher()
    
    # 示例文档ID（请替换为实际文档ID）
    doc_id = "your_document_id_here"
    
    # 获取文档内容
    doc_content = fetcher.get_document(doc_id)
    
    print("文档内容:")
    print(doc_content)
    
    # 导出为JSON文件
    fetcher.export_to_json(doc_content, "output/document.json")


def example_api():
    """
    使用API方式获取文档
    """
    print("=== 使用飞书API获取文档 ===")
    
    # 初始化fetcher
    fetcher = FeishuAPIFetcher()
    
    # 示例文档ID（请替换为实际文档ID）
    doc_id = "your_document_id_here"
    
    # 获取文档内容
    doc_content = fetcher.get_document(doc_id)
    
    print("文档内容:")
    print(doc_content)
    
    # 获取文档块信息
    doc_blocks = fetcher.get_document_blocks(doc_id)
    
    print("\n文档块信息:")
    print(doc_blocks)


def main():
    """
    主函数
    """
    print("飞书文档获取示例")
    print("=" * 50)
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 选择方式
    print("请选择获取方式:")
    print("1. 使用飞书CLI")
    print("2. 使用飞书API")
    
    choice = input("请输入选择 (1/2): ").strip()
    
    if choice == "1":
        example_cli()
    elif choice == "2":
        example_api()
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()