#!/usr/bin/env python3
"""
初始化脚本 - 创建测试数据
"""
import pandas as pd
from pathlib import Path
import random

def create_sample_data():
    """创建样本数据文件"""
    data_dir = Path(__file__).parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 北京销售数据
    beijing_data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'product': ['iPhone', 'MacBook', 'iPad', 'AirPods', 'Apple Watch'],
        'quantity': [5, 2, 8, 15, 10],
        'price': [6999, 9999, 2999, 999, 2499],
        'store': ['Beijing-A', 'Beijing-A', 'Beijing-B', 'Beijing-A', 'Beijing-B']
    }
    
    # 上海销售数据
    shanghai_data = {
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'product': ['MacBook Pro', 'iPhone 15', 'iPad Air', 'AirPods Max', 'MacBook Air'],
        'quantity': [3, 10, 6, 4, 5],
        'price': [12999, 5999, 4799, 4399, 8999],
        'store': ['Shanghai-1', 'Shanghai-1', 'Shanghai-2', 'Shanghai-1', 'Shanghai-2']
    }
    
    # 保存数据
    pd.DataFrame(beijing_data).to_csv(data_dir / "sales_beijing.csv", index=False)
    pd.DataFrame(shanghai_data).to_csv(data_dir / "sales_shanghai.csv", index=False)
    
    print(f"已创建样本数据: {list(data_dir.glob('*.csv'))}")


if __name__ == "__main__":
    create_sample_data()
