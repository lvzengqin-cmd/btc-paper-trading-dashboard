#!/usr/bin/env python3
"""
自动同步数据到 GitHub Pages
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/paper_trading/accounts.json")
DST = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/realtime_dashboard/accounts.json")

def sync():
    if not SRC.exists():
        return
    
    with open(SRC, 'r') as f:
        data = json.load(f)
    
    data['_last_updated'] = datetime.now().isoformat()
    
    with open(DST, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Git 操作
    subprocess.run(['git', 'add', 'accounts.json'], cwd=DST.parent, capture_output=True)
    subprocess.run(['git', 'commit', '-m', f'Update: {datetime.now().strftime("%H:%M:%S")}'], cwd=DST.parent, capture_output=True)
    result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=DST.parent, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 已同步到 GitHub Pages: {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"⚠️ 推送失败")

if __name__ == "__main__":
    sync()
