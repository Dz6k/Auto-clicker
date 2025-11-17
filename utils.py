import os
from typing import NoReturn
class Config:
    def __init__(self) -> NoReturn:
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
