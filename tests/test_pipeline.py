"""
测试模块
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_cleaning import remove_duplicates, fill_missing_values, validate_data
from src.data_merge import add_calculated_fields


class TestDataCleaning:
    """数据清洗测试"""
    
    def test_remove_duplicates(self):
        """测试删除重复行"""
        df = pd.DataFrame({
            'name': ['Alice', 'Alice', 'Bob', 'Bob'],
            'age': [25, 25, 30, 30]
        })
        result = remove_duplicates(df)
        assert len(result) == 2
    
    def test_fill_missing_values(self):
        """测试填充缺失值"""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', None],
            'quantity': [10, None, 20],
            'price': [100, 200, 300]
        })
        config = {'process': {'numeric_columns': ['quantity', 'price']}}
        result = fill_missing_values(df, config)
        assert result['name'].isna().sum() == 0
        assert result['quantity'].isna().sum() == 0
    
    def test_validate_data(self):
        """测试数据验证"""
        df = pd.DataFrame({
            'date': ['2024-01-01', 'invalid-date', '2024-01-03'],
            'quantity': [10, 20, -5],  # -5 应该是无效的
            'price': [100, 200, 300]
        })
        config = {'process': {'date_column': 'date', 'numeric_columns': ['quantity', 'price']}}
        result = validate_data(df, config)
        assert len(result) == 2  # 只保留有效的行


class TestDataMerge:
    """数据合并测试"""
    
    def test_add_calculated_fields(self):
        """测试添加计算字段"""
        df = pd.DataFrame({
            'quantity': [2, 3, 4],
            'price': [10, 20, 30]
        })
        result = add_calculated_fields(df)
        assert 'revenue' in result.columns
        assert result['revenue'].tolist() == [20, 60, 120]


class TestDataPipeline:
    """完整流水线测试"""
    
    def test_pipeline_execution(self):
        """测试流水线能否成功执行"""
        from main import run_pipeline
        
        # 这个测试需要数据文件存在
        # 在CI环境中会自动创建测试数据
        result = run_pipeline()
        assert 'row_count' in result
        assert 'columns' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
