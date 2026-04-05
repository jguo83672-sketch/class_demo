"""
数据入库模块
将处理后的数据加载到数据库
"""

import pandas as pd
import sqlite3
import logging
from pathlib import Path
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_database(db_path: str, table_name: str) -> sqlite3.Connection:
    """初始化数据库连接"""
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    logger.info(f"数据库连接成功: {db_path}")
    return conn


def load_to_database(csv_file: str, db_path: str, table_name: str) -> int:
    """将CSV数据加载到数据库"""
    logger.info(f"开始加载数据到数据库...")

    # 读取CSV
    df = pd.read_csv(csv_file)
    logger.info(f"读取CSV: {len(df)} 行")

    # 连接数据库
    conn = init_database(db_path, table_name)

    # 加载到数据库（先删除旧表）
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # 保存到数据库
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # 验证
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    logger.info(f"数据入库完成！共 {count} 条记录")
    return count


def query_sample(db_path: str, table_name: str, limit: int = 5) -> pd.DataFrame:
    """查询样本数据"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
    conn.close()
    return df


def get_data_summary(db_path: str, table_name: str) -> dict:
    """获取数据摘要"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 行数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    # 列信息
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    conn.close()

    return {"row_count": row_count, "columns": [col[1] for col in columns]}


if __name__ == "__main__":
    print("数据入库模块测试")
    print("=" * 50)
