#!/usr/bin/env python3
"""
在 WSL (Blue Bull Bot) 上運行此腳本以導出 CSD n8n workflow
使用: python3 export_wsl_n8n.py
"""
import sqlite3, json, os, sys

db_paths = [
    os.path.expanduser("~/.n8n/database.sqlite"),
    "/home/joegolflui/.n8n/database.sqlite",
    "/home/emofficemba/.n8n/database.sqlite",
]

db_path = None
for p in db_paths:
    if os.path.exists(p):
        db_path = p
        print(f"找到資料庫: {p}")
        break

if not db_path:
    print("找不到 n8n 資料庫，請確認路徑")
    sys.exit(1)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT name, nodes, connections, settings, staticData FROM workflow_entity WHERE name LIKE '%CSD%'")
rows = c.fetchall()

if not rows:
    print("找不到 CSD workflow，可用 workflow 列表:")
    c.execute("SELECT name FROM workflow_entity")
    for r in c.fetchall():
        print(f"  - {r[0]}")
    sys.exit(1)

out_dir = os.path.expanduser("~/ai-influencer-automation/n8n-workflows")
os.makedirs(out_dir, exist_ok=True)

for r in rows:
    name, nodes, connections, settings, staticData = r
    wf = {
        "name": name,
        "nodes": json.loads(nodes) if nodes else [],
        "connections": json.loads(connections) if connections else {},
        "settings": json.loads(settings) if settings else {},
        "staticData": json.loads(staticData) if staticData else None,
        "tags": []
    }
    fname = os.path.join(out_dir, name.replace(" ", "_").replace("/", "_") + ".json")
    with open(fname, "w") as f:
        json.dump(wf, f, indent=2, ensure_ascii=False)
    print(f"✅ 導出: {fname}")

conn.close()
print("\n完成！請在 ai-influencer-automation 目錄 git add + commit + push")
