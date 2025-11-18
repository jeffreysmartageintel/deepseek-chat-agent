# 修复依赖冲突问题

## 问题说明

安装依赖时出现警告，因为系统中存在旧的 `langchain 0.1.0` 包，与新安装的包不兼容。

## 解决方案

### 步骤 1: 卸载旧的 langchain 包

在 PowerShell 中运行（确保虚拟环境已激活）：

```powershell
pip uninstall langchain -y
```

### 步骤 2: 验证安装

运行以下命令检查是否还有冲突：

```powershell
pip check
```

### 步骤 3: 测试运行

```powershell
python -m app.main
```

## 说明

- `langchain 0.1.0` 是旧版本，已被 `langchain-classic` 和 `langchain-community` 替代
- 警告不会影响功能，但建议卸载旧包以避免潜在问题
- 如果卸载后出现问题，可以重新安装：`pip install langchain==0.1.0`（但不推荐）

