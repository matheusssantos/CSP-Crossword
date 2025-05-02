import time
from termcolor import colored
import re

def load_word_list(path: str) -> list[str]:
  with open(path, 'r', encoding='utf-8') as f:
    return [line.strip().upper() for line in f if line.strip()]

def contains_num(word: str) -> bool:
  return bool(re.search(r'\d+(\.\d+)?', word))

class Timer:
  def __init__(self, timer_name: str):
    self.name = timer_name
    self.result = 0
    
  def start(self) -> None:
    self.result = time.time()
    
  def end(self) -> None:
    end_time = time.time()
    self.result = end_time - self.result
    
  def print_response(self) -> None:
    LOG_SYSTEM(f"{self.name}: {self.result:.2f} segundos")
    

def logger_factory(log_type: str, color: str = 'white'):
  def log(message: str) -> None:
    print(colored(f"[{log_type}] {message}", color))
  return log

LOG_ERROR = logger_factory("ERROR", 'red')
LOG_SYSTEM = logger_factory("SYSTEM", 'cyan')
