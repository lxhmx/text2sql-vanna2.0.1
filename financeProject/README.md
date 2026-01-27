# Finance Project

基于 **FastAPI + MySQL** 的财务考勤自助报表项目，前端使用 **Vue 3 + Vite**（目录 `font-vue`）。

## 功能概览
- 用户注册 / 登录，JWT 鉴权。
- 考勤、加班、工时的录入与查询。
- 加班时长统计与扣款计算。
- 开箱即用的前后端分离架构，含 OpenAPI 文档（`/docs`）。

## 后端快速启动
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy config_template.py config.py  # Windows
# 按需填写数据库、JWT 密钥等配置
uvicorn app:app --reload
```

### 数据库初始化
在 MySQL 创建数据库后执行：
```sql
SOURCE database/init_tables.sql;
SOURCE database/chat_tables.sql;
SOURCE database/sql/attendance_deduction_tables.sql;
SOURCE database/sql/employee_overtime.sql;
```

## 前端启动（开发模式）
```bash
cd font-vue
npm install
npm run dev
```
构建生产包：`npm run build`，Nginx 配置示例见 `font-vue/nginx.conf`。

## 目录结构
- `api/`：业务 API（考勤、加班、工时）
- `common/`：数据库连接、日志、依赖与安全
- `database/`：SQL 脚本与客户端
- `schemas/`：Pydantic 模型
- `font-vue/`：前端工程

## 部署提示
- 将 `config.py` 中的密钥与数据库凭据使用环境变量或安全存储管理。
- 生产部署建议使用 `uvicorn --host 0.0.0.0 --port 8000` 或搭配 Gunicorn + UvicornWorkers。
