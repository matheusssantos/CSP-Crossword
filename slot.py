class Slot:
  def __init__(self, row: int, col: int, value: str):
    self.row = row
    self.col = col
    self.value = value
    
  def __repr__(self):
    return self.value