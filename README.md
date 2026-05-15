# NetBloom - 人物关系图谱编辑器

**在线地址：** https://netbloom.1tik.top/edit.html（编辑版）/ https://netbloom.1tik.top/graph.html（查看版）

---

## 2026-05-15 更新（Phase 3.5 — 编辑器细节打磨）

### 更改关系类型颜色弹窗优化
- **关系类型按色相排序**：弹窗内各关系类型按颜色的 Hue 值从小到大排列
- **十六色面板 2×8 布局**：颜色选择从竖排改为 2行×8列网格，与颜色筛选下拉保持一致
- **十六色顺序统一按色相排序**：弹窗十六色与筛选下拉中的十六色完全一致
- **移除 input[type=color]**：不再需要原生取色器，直接点击圆形色块即可切换颜色

### 关系列表搜索功能
- **姓名模糊搜索**：支持按关系起点或终点人物名模糊过滤
- **搜索空状态提示**：找不到结果时显示"找不到你要搜的人哦~"
- **修复三元表达式语法错误**：修复 filter 函数中缺少 else 分支导致的 JS 语法错误

### 筛选下拉全面升级
- **关系类型筛选**（relTypeFilter）：替换原生 select 为自定义下拉（背景 rgba(10,15,35,0.98)，选项前带关系颜色圆点）
- **人物标签筛选**（charTagFilter）：同样升级为自定义下拉
- **下拉面板超出屏幕处理**：按钮位置空间不够时自动翻转显示在上方
- **16 颜色网格下拉**：标签颜色、关系颜色筛选均用 4×4 网格面板，支持边界检测

---

## 2026-05-14 更新（Phase 3 — 编辑器交互体验升级）

### 重大改进

**1. 添加分组/标签改为弹窗选择**
- 「添加分组」和「添加标签」从内联表单卡片改为点击按钮弹窗选择
- 弹窗内含名称输入框 + 颜色选择器（16色网格）
- 新增 `openAddGroupModal` / `closeAddGroupModal` / `confirmAddAddGroup` 函数
- 新增 `openAddTagModal` / `closeAddTagModal` / `confirmAddTag` 函数

**2. 下拉颜色选择器优化**
- 统一改为下拉面板（4×4=16 颜色网格），不再平铺展示
- 所有下拉统一用 `closeAllColorDropdowns()` 关闭前一个再打开新的
- `toggleColorDropdown(id, type)` 支持 `group` / `tag` / `relType` / `modalGroup` / `modalTag` 五种类型
- 颜色色相（Hue）排序：彩虹顺序从红→橙→黄→绿→青→蓝→紫→粉

**3. 所有颜色列表按色相排序**
- 标签列表（updateTagList）
- 标签选择（updateTagSelect）
- 人物编辑弹窗标签（editCharTagWrap）
- 人物编辑弹窗分组（editCharGroupWrap）
- 关系类型管理列表（改色弹窗内）

**4. onclick 变量引用修复**
- `onclick="openEditGroupColor(${id})"` → `onclick="openEditGroupColor('${id}')"`（加引号）
- `onclick="deleteGroup(${id})"` → `onclick="deleteGroup('${id}')"`
- `onclick="openEditTagColor(${id})"` → `onclick="openEditTagColor('${id}')"`
- `onclick="deleteTag(${id})"` → `onclick="deleteTag('${id}')"`
- `onclick="toggleCharTag(${id})"` → `onclick="toggleCharTag('${id}')"`
- 根因：ID 字符串如 `g_1778750846326` 被渲染成 JS 变量引用，加引号后变成字符串

---

## 功能特性

### 图谱编辑器
- **D3.js 力导向图**：自动布局，节点自动排列，支持多条平行边弧形展示
- **节点大小**：根据关系数量动态调整（每2条关系+3px，范围12-40px）
- **拖拽编辑**：拖拽节点调整位置
- **缩放平移**：鼠标滚轮缩放，拖拽空白处平移
- **关系连线**：支持多种关系类型（师徒、亲友、敌对等）
- **节点分组**：按门派/阵营自动分组着色

### 编辑功能
- **新建/删除人物**：快速添加或删除节点
- **新建/删除关系**：连接两个节点建立关系
- **人物信息**：支持添加人物描述和分组标签
- **关系描述**：为每条关系添加详细说明
- **重命名图谱**：随时修改图谱名称

### 筛选与搜索
- **颜色筛选**：标签颜色、关系颜色双重过滤
- **类型筛选**：关系类型下拉筛选
- **姓名搜索**：关系列表按起点/终点人物名模糊搜索
- **标签筛选**：人物列表按标签快速过滤

### 界面布局
- **可折叠编辑面板**：点击全屏预览按钮收起左侧面板
- **右侧抽屉式编辑面板**：分组/标签/关系/人物四tab切换
- **悬浮保存按钮**：每个tab底部 sticky 保存按钮
- **右键菜单**：双击节点打开编辑/删除菜单

### 云端同步
- **自动保存**：每10秒自动保存到云端
- **手动同步**：支持手动触发保存
- **图谱列表**：查看和管理所有云端图谱

---

## 技术栈

- **前端**：原生 HTML + CSS + JavaScript
- **图形库**：D3.js v7（力导向图）
- **后端**：Python Flask
- **数据库**：SQLite
- **服务器**：阿里云 + Nginx

---

## 文件结构

```
netbloom/
├── edit.html        # 图谱编辑器（当前开发版本）
├── graph.html       # 图谱查看版（生产部署）
├── server.py        # Flask 后端
├── data.db          # SQLite 数据库
└── backups/         # 本地备份
```

---

## 工作流程

1. 本地 dev 分支迭代 `edit.html`
2. 测试通过后上传服务器 `/var/www/netbloom/edit.html`
3. 同步到 `/var/www/netbloom-git/` 并 push 到 GitHub main 分支

**服务器信息：**
- SSH：`root@47.245.98.9`
- 生产目录：`/var/www/netbloom/`
- Git 工作目录：`/var/www/netbloom-git/`