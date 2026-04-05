# Python 数据处理 CI/CD 项目

一个基于 GitHub Actions 的数据处理自动化流水线项目。

## 项目简介

本项目演示了如何使用 GitHub Actions 实现数据清洗、合并、入库的 CI/CD 自动化流程。

### 功能特性

- **数据清洗**: 自动处理缺失值、重复数据、异常值
- **数据合并**: 合并多个数据源为一个统一数据集
- **数据入库**: 将处理后的数据加载到 SQLite 数据库
- **自动化测试**: 完整的单元测试覆盖
- **CI/CD 流水线**: 代码提交自动触发完整流程

## 项目结构

```
.
├── data/                      # 数据目录
│   ├── raw/                   # 原始数据
│   │   ├── sales_beijing.csv
│   │   ├── sales_shanghai.csv
│   │   └── sales_shenzhen.csv
│   ├── processed/             # 处理后的数据
│   └── warehouse/             # 数据库
├── src/                       # 源代码
│   ├── data_cleaning.py       # 数据清洗
│   ├── data_merge.py          # 数据合并
│   └── data_load.py           # 数据入库
├── tests/                     # 测试文件
│   └── test_pipeline.py
├── .github/workflows/         # GitHub Actions
│   └── ci-cd-pipeline.yml
├── config.yaml                # 配置文件
├── main.py                    # 主程序入口
└── requirements.txt           # 依赖
```

## 本地运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行数据处理流水线

```bash
python main.py
```

### 3. 运行测试

```bash
pytest tests/ -v
```

## CI/CD 流水线说明

### 流水线阶段

1. **Code Quality Check** - 代码质量检查
   - Flake8 代码风格检查
   - Black 格式化验证

2. **Unit Tests** - 单元测试
   - 运行所有测试用例
   - 生成覆盖率报告

3. **Data Pipeline** - 数据处理流水线
   - 数据清洗
   - 数据合并
   - 数据入库
   - 验证输出结果

4. **Deploy** - 部署 (仅 main 分支)
   - 创建生产环境
   - 最终验证

### 触发条件

- 推送到 `main` 或 `develop` 分支
- Pull Request 到 `main` 分支
- 手动触发 (`workflow_dispatch`)

## GitHub Actions 故障排查

### 常见问题

1. **测试失败**: 检查测试用例是否正确
2. **流水线错误**: 查看 Actions 日志
3. **依赖问题**: 确保 `requirements.txt` 完整

### 故意破坏练习

如需练习修复流水线，可以：

1. **破坏代码**: 修改源代码引入错误
2. **破坏配置**: 修改 `config.yaml`
3. **破坏数据**: 修改测试数据格式

## 作者

郭家霖 225020508

## 许可证

MIT License
