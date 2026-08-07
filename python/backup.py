import shutil
import os
import glob
from datetime import datetime

def backup_database():

    source = "database/qinxiang_store.db"

    if not os.path.exists("backup"):
        os.mkdir("backup")

    filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    destination = f"backup/qinxiang_store_{filename}.db"

    shutil.copy2(source, destination)

    files = glob.glob("backup/*.db")

    files.sort(key=os.path.getmtime)

    while len(files) > 30:

        os.remove(files[0])

        files.pop(0) 
        
    print("✅ 資料庫已備份")