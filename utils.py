import time

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
    print(f"{self.name}: {self.result:.2f} segundos")