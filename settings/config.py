#######################################################################################
# Param Data @
# Return @
# TODO @ 模板配置项
# *
# !
# ?
#######################################################################################

import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only

load_dotenv()
load_dotenv(verbose=True)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

HOST_IP = os.getenv("HOST_IP")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
