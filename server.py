#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网罗众生 - 人物关系图谱编辑器
Flask 后端服务

功能：
- 图谱数据的 CRUD 操作
- SQLite 数据库存储

启动：python server.py
默认端口：5000
"""

import os
import sys
import json
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS

# 添加中文处理
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 数据库配置
DATABASE = os.path.join(os.path.dirname(__file__), 'data.db')


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """初始化数据库"""
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()
        print(f"数据库初始化完成: {DATABASE}")


# ==================== API 路由 ====================

@app.route('/api/graphs', methods=['GET'])
def get_graphs():
    """获取所有图谱列表"""
    db = get_db()
    cursor = db.execute(
        'SELECT id, name, data, updated_at FROM graphs ORDER BY updated_at DESC'
    )
    graphs = []
    for row in cursor.fetchall():
        data = json.loads(row['data'])
        graphs.append({
            'id': row['id'],
            'name': row['name'],
            'updated_at': row['updated_at'],
            'node_count': len(data.get('nodes', [])),
            'link_count': len(data.get('links', []))
        })
    return jsonify({'graphs': graphs})


@app.route('/api/graphs/<graph_id>', methods=['GET'])
def get_graph(graph_id):
    """获取指定图谱的完整数据"""
    db = get_db()
    cursor = db.execute(
        'SELECT id, name, data, updated_at FROM graphs WHERE id = ?',
        (graph_id,)
    )
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': '图谱不存在'}), 404
    
    return jsonify({
        'id': row['id'],
        'name': row['name'],
        'updated_at': row['updated_at'],
        'data': json.loads(row['data'])
    })


@app.route('/api/graphs', methods=['POST'])
def create_graph():
    """创建新图谱"""
    body = request.get_json()
    
    if not body or 'data' not in body:
        return jsonify({'error': '缺少图谱数据'}), 400
    
    graph_id = str(uuid.uuid4())
    name = body.get('name', '未命名图谱')
    data = body['data']
    
    # 如果没有graphName，用name
    if not data.get('graphName'):
        data['graphName'] = name
    
    db = get_db()
    db.execute(
        'INSERT INTO graphs (id, name, data, updated_at) VALUES (?, ?, ?, ?)',
        (graph_id, name, json.dumps(data, ensure_ascii=False), datetime.now().isoformat())
    )
    db.commit()
    
    return jsonify({
        'id': graph_id,
        'name': name,
        'message': '创建成功'
    }), 201


@app.route('/api/graphs/<graph_id>', methods=['PUT'])
def update_graph(graph_id):
    """保存/更新图谱数据"""
    body = request.get_json()
    
    if not body or 'data' not in body:
        return jsonify({'error': '缺少图谱数据'}), 400
    
    name = body.get('name')
    data = body['data']
    
    # 如果没有graphName，用name
    if not data.get('graphName') and name:
        data['graphName'] = name
    
    db = get_db()
    
    # 检查图谱是否存在
    cursor = db.execute('SELECT id FROM graphs WHERE id = ?', (graph_id,))
    if not cursor.fetchone():
        return jsonify({'error': '图谱不存在'}), 404
    
    # 更新数据
    db.execute(
        'UPDATE graphs SET name = ?, data = ?, updated_at = ? WHERE id = ?',
        (name or data.get('graphName', '未命名'), json.dumps(data, ensure_ascii=False), datetime.now().isoformat(), graph_id)
    )
    db.commit()
    
    return jsonify({'message': '保存成功'})


@app.route('/api/graphs/<graph_id>', methods=['DELETE'])
def delete_graph(graph_id):
    """删除图谱"""
    db = get_db()
    
    # 检查图谱是否存在
    cursor = db.execute('SELECT id FROM graphs WHERE id = ?', (graph_id,))
    if not cursor.fetchone():
        return jsonify({'error': '图谱不存在'}), 404
    
    db.execute('DELETE FROM graphs WHERE id = ?', (graph_id,))
    db.commit()
    
    return jsonify({'message': '删除成功'})


# ==================== 静态文件 ====================

@app.route('/')
def index():
    """返回编辑器页面"""
    return send_from_directory('.', 'editor.html')


@app.route('/preview')
def preview():
    """返回预览页面"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    """静态文件服务"""
    return send_from_directory('.', filename)


# ==================== 启动 ====================

if __name__ == '__main__':
    # 初始化数据库
    if not os.path.exists(DATABASE):
        init_db()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"启动服务: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
