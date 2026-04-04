"""
数据合并模块
将多个数据源合并成一个统一的数据集
"""
import pandas as pd
import logging
from pathlib import Path
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_multiple_files(pattern: str) -> list:
    """加载多个匹配的文件"""
    files = glob.glob(pattern)
    logger.info(f"找到 {len(files)} 个文件: {files}")
    return files


def merge_sales_data(data_dir: str, output_file: str) -> pd.DataFrame:
    """合并销售数据"""
    logger.info(f"开始合并数据，目录: {data_dir}")
    
    # 查找所有清洗后的CSV文件
    pattern = str(Path(data_dir) / "*.csv")
    files = load_multiple_files(pattern)
    
    if not files:
        logger.warning("没有找到要合并的文件")
        return pd.DataFrame()
    
    # 读取并合并所有文件
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        df['source_file'] = Path(file).stem
        dfs.append(df)
        logger.info(f"加载: {file}, 行数: {len(df)}")
    
    # 合并所有数据
    merged_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"合并完成，总行数: {len(merged_df)}")
    
    # 添加合并后的统计
    logger.info(f"数据列: {list(merged_df.columns)}")
    
    # 保存合并结果
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(output_path, index=False)
    logger.info(f"合并数据已保存: {output_file}")
    
    return merged_df


def add_calculated_fields(df: pd.DataFrame) -> pd.DataFrame:
    """添加计算字段"""
    if 'quantity' in df.columns and 'price' in df.columns:
        df['revenue'] = df['quantity'] * df['price']
        logger.info("添加了 'revenue' 计算字段")
    
    return df


if __name__ == "__main__":
    print("数据合并模块测试")
    print("=" * 50)
