import os
from typing import NoReturn
from dataclasses import dataclass
import json

@dataclass
class Var:
    interval: float
    variation: float
    time_bump: float
    
    
class Default:
    data: dict = {
        "interval": 0.022,
        "variation": 0.0015,
        "time_bump": 1.0
    }
    
    
class Config:
    def __init__(self) -> NoReturn:
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    def create(self) -> NoReturn:
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(Default.data, f, ensure_ascii=False, indent=4)

    def load(self) -> Var:
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
             
            return Var(
                interval=data.get('interval', Default.data['interval']),
                variation=data.get('variation', Default.data['variation']),
                time_bump=data.get('time_bump', Default.data['time_bump'])
            )
            