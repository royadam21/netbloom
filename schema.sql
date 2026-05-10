-- 图谱主表
CREATE TABLE IF NOT EXISTS graphs (
    id TEXT PRIMARY KEY,          -- UUID
    name TEXT NOT NULL,           -- 图谱名称
    data TEXT NOT NULL,           -- JSON字符串（完整的图谱数据）
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 索引：按更新时间排序
CREATE INDEX IF NOT EXISTS idx_graphs_updated_at ON graphs(updated_at DESC);
