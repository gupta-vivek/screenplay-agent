import os
from dotenv import load_dotenv

load_dotenv()

# LANCEDB
LANCEDB_URI=os.getenv("LANCEDB_URI", None)
LANCEDB_API_KEY=os.getenv("LANCEDB_API_KEY", None)
LANCEDB_REGION=os.getenv("LANCEDB_REGION", None)
LANCEDB_TABLE_NAME=os.getenv("LANCEDB_TABLE_NAME", None)

# EMBEDDING MODEL
EMBEDDING_MODEL="all-mpnet-base-v2"

# DEEPSEEK MODEL
DEEPSEEK_MODEL="deepseek-chat"