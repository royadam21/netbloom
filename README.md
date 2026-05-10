# NetBloom - 人物关系图谱编辑器

一个基于 D3.js 力导向图的可视化人物关系图谱编辑器，支持自定义节点、关系、群组，适合用于小说、游戏、影视等内容的人物关系梳理。

## 🌐 在线访问

**编辑器**: https://netbloom.1tik.top/editor.html

## 功能特性

- **节点管理** - 添加、编辑、删除人物节点，支持头像、群组标签
- **关系管理** - 创建双向/单向关系，定义关系类型（如"师徒"、"夫妻"、"仇敌"）
- **群组管理** - 按阵营/门派/家族等分类节点，支持颜色区分
- **交互探索** - 拖拽节点、缩放视图、力导向自动布局
- **数据持久化** - 保存到云端数据库，支持图谱列表管理
- **导入工具** - 批量导入人物/关系数据

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | D3.js v7 (力导向图), 原生 JavaScript |
| 后端 | Python Flask |
| 数据库 | SQLite |
| 部署 | nginx + gunicorn |
| 域名 | 1tik.top |

## 文件结构

```
.
├── editor.html       # 主编辑器页面（D3 图谱可视化 + 交互界面）
├── import-tool.html # 数据导入工具
├── index.html        # 图谱列表页
├── server.py         # Flask 后端（API 接口）
├── package.json      # 项目配置
├── schema.sql        # 数据库结构
├── prd.md           # 产品需求文档
└── data.db          # SQLite 数据库
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/graphs` | 获取图谱列表 |
| POST | `/api/graphs` | 创建新图谱 |
| GET | `/api/graphs/<id>` | 获取图谱详情 |
| PUT | `/api/graphs/<id>` | 更新图谱 |
| DELETE | `/api/graphs/<id>` | 删除图谱 |
| POST | `/api/upload` | 上传图片 |

## 开发

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/royadam21/netbloom.git
cd netbloom

# 安装依赖
pip install flask

# 启动后端
python server.py

# 打开 editor.html
# 或 nginx 配置代理到 http://localhost:5000
```

### 部署架构

```
用户浏览器
    ↓ https://netbloom.1tik.top
nginx (47.245.98.9:80)
    ↓ /api → localhost:5002
Flask (Gunicorn)
    ↓
SQLite (data.db)
```

## License

MIT