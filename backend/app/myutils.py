import json
from typing import List

def arr2json(arr: List[str]) -> str:
    return json.dumps(arr)