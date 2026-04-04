"""
主程序入口
执行完整的数据处理流水线：清洗 -> 合并 -> 入库
"""
import sys
import logging
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_cleaning import clean_data
from src.data_merge import merge_sales_data, add_calculated_fields
from src.data_load import load_to_database, get_data_summary, load_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline():
    """运行完整的数据处理流水线"""
    logger.info("=" * 60)
    logger.info("开始执行数据处理流水线")
    logger.info("=" * 60)
    
    config = load_config()
    data_dir = Path(__file__).parent / config['data']['input_dir']
    output_dir = Path(__file__).parent / config['data']['output_dir']
    
    # Step 1: 数据清洗
    logger.info("\n[Step 1/3] 数据清洗")
    logger.info("-" * 40)
    
    cleaned_files = []
    for csv_file in data_dir.glob("*.csv"):
        output_file = output_dir / f"cleaned_{csv_file.name}"
        try:
            clean_data(str(csv_file), str(output_file))
            cleaned_files.append(str(output_file))
        except Exception as e:
            logger.error(f"清洗文件 {csv_file.name} 失败: {e}")
    
    # Step 2: 数据合并
    logger.info("\n[Step 2/3] 数据合并")
    logger.info("-" * 40)
    
    merged_file = output_dir / "merged_sales.csv"
    if cleaned_files:
        merged_df = merge_sales_data(str(output_dir), str(merged_file))
        merged_df = add_calculated_fields(merged_df)
        merged_df.to_csv(merged_file, index=False)
        logger.info(f"合并数据已更新: {merged_file}")
    
    # Step 3: 数据入库
    logger.info("\n[Step 3/3] 数据入库")
    logger.info("-" * 40)
    
    db_path = Path(__file__).parent / config['database']['path']
    table_name = config['database']['table']
    
    row_count = load_to_database(str(merged_file), str(db_path), table_name)
    
    # 显示数据摘要
    logger.info("\n" + "=" * 60)
    logger.info("流水线执行完成！")
    logger.info("=" * 60)
    
    summary = get_data_summary(str(db_path), table_name)
    logger.info(f"数据库: {db_path}")
    logger.info(f"表名: {table_name}")
    logger.info(f"总记录数: {summary['row_count']}")
    logger.info(f"字段: {summary['columns']}")
    
    return summary


if __name__ == "__main__":
    run_pipeline()
