#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/paper_trading/accounts.json")
SIGNALS_SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/signals_history.json")
DST = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/realtime_dashboard/accounts.json")

def sync():
    # 同步账户数据
    if SRC.exists():
        with open(SRC, 'r') as f:
            data = json.load(f)
        
        data['_last_updated'] = datetime.now().isoformat()
        
        # 同步信号历史
        if SIGNALS_SRC.exists():
            with open(SIGNALS_SRC, 'r') as f:
                data['signals_history'] = json.load(f)
        
        with open(DST, 'w') as f:
            json.dump(data, f, indent=2)
    
    os.chdir(DST.parent)
    subprocess.run(['git', 'add', 'accounts.json'], capture_output=True)
    subprocess.run(['git', 'commit', '-m', f'Update: {datetime.now().strftime("%H:%M:%S")}'], capture_output=True)
    result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 已同步到 GitHub Pages: {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"⚠️ 推送失败")

if __name__ == "__main__":
    sync()
