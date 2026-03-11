import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# DBファイルの場所
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "database.db")

# レベルと必要ポイント
LEVEL_ROLE_RULES = {
    1: 0,
    2: 50,
    3: 200,
    4: 400,
}

# ロール名
LEVEL_ROLE_NAMES = {
    1: "Lv.1 素人のかめさん",
    2: "Lv.2 普通のかめさん",
    3: "Lv.3 玄人のかめさん",
    4: "Lv.4 ベテランのかめさん",
}