"""
数据清洗模块
处理缺失值、异常值、重复数据等
"""
import pandas as pd
import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_data(file_path: str) -> pd.DataFrame:
    """加载原始数据"""
    logger.info(f"加载数据文件: {file_path}")
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    logger.info(f"加载了 {len(df)} 行数据")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """删除重复行"""
    original_len = len(df)
    df = df.drop_duplicates()
    removed = original_len - len(df)
    logger.info(f"删除了 {removed} 行重复数据")
    return df


def fill_missing_values(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """填充缺失值"""
    numeric_cols = config.get('process', {}).get('numeric_columns', [])
    
    for col in df.columns:
        if col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna('Unknown')
    
    logger.info(f"填充了缺失值")
    return df


def validate_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """数据验证和清洗"""
    # 检查日期列
    date_col = config.get('process', {}).get('date_column')
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        # 删除日期无效的行
        df = df.dropna(subset=[date_col])
        logger.info(f"处理日期列: {date_col}")
    
    # 数值列不能为负
    numeric_cols = config.get('process', {}).get('numeric_columns', [])
    for col in numeric_cols:
        if col in df.columns:
            df = df[df[col] >= 0]
    
    logger.info(f"数据验证后剩余 {len(df)} 行")
    return df


def clean_data(input_file: str, output_file: str) -> pd.DataFrame:
    """完整的数据清洗流程"""
    config = load_config()
    
    # 加载数据
    df = load_data(input_file)
    
    # 删除重复
    if config.get('process', {}).get('remove_duplicates', True):
        df = remove_duplicates(df)
    
    # 填充缺失值
    if config.get('process', {}).get('fill_missing', True):
        df = fill_missing_values(df, config)
    
    # 数据验证
    df = validate_data(df, config)
    
    # 保存清洗后的数据
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"清洗后的数据已保存: {output_file}")
    
    return df


if __name__ == "__main__":
    # 测试清洗功能
    print("数据清洗模块测试")
    print("=" * 50)
