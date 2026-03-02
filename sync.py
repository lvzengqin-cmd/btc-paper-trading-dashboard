#!/usr/bin/env python3
import json
import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# 源文件路径
SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/paper_trading/accounts.json")
SIGNALS_SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/signals_history.json")
MONITOR_MSG_SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/monitor_messages.json")
BTC_PRICE_SRC = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/btc_price.json")

# 目标目录
DST_DIR = Path("/root/.openclaw/workspace/skills/btc-long-short-analysis/realtime_dashboard")
DST = DST_DIR / "accounts.json"

def sync():
    updated = False
    
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
        updated = True
    
    # 同步监控消息
    if MONITOR_MSG_SRC.exists():
        shutil.copy2(MONITOR_MSG_SRC, DST_DIR / "monitor_messages.json")
        updated = True
    
    # 同步BTC价格
    if BTC_PRICE_SRC.exists():
        shutil.copy2(BTC_PRICE_SRC, DST_DIR / "btc_price.json")
        updated = True
    
    # Git提交和推送
    if updated:
        os.chdir(DST_DIR)
        subprocess.run(['git', 'add', '-A'], capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Update: {datetime.now().strftime("%H:%M:%S")}'], capture_output=True)
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 已同步到 GitHub Pages: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"⚠️ 推送失败: {result.stderr}")
    else:
        print(f"⏭️ 无更新: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    sync()
