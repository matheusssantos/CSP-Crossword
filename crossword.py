
from slot import Slot
from word import Word


class Crossword:
  def __init__(self, grid_file_path: str):
    self.grid: list[list[str]] = []                 
    self.slots: list[Slot] = []
    self.words: list[Word] = []
    self._load_grid(grid_file_path)
    
  def _load_grid(self, path: str) -> None:
    with open(path, 'r') as f:
      self.grid = [list(line.strip()) for line in f if line.strip()]
    
  def print_grid(self) -> None:
    for row in self.grid:
      print("".join(row))
      
  def generate_slots(self):
    for i, row in enumerate(self.grid):
      for j, cell in enumerate(row):
        if cell == "?":
          slot = Slot(i, j, None)
          self.slots.append(slot)
          
  def extract_words(self):
    self.words = []

    # Horizontal
    for i, row in enumerate(self.grid):
      current_slots = []
      for j, cell in enumerate(row + ['.']):
        if cell == '?':
          current_slots.append(self._get_slot(i, j))
        else:
          if len(current_slots) > 1:
            self.words.append(Word(current_slots))
          current_slots = []

    # Vertical
    cols = len(self.grid[0])
    rows = len(self.grid)
    for j in range(cols):
      current_slots = []
      for i in range(rows + 1):
        cell = self.grid[i][j] if i < rows else '.'
        if cell == '?':
          current_slots.append(self._get_slot(i, j))
        else:
          if len(current_slots) > 1:
            self.words.append(Word(current_slots))
          current_slots = []

  def _get_slot(self, i: int, j: int) -> Slot:
    for slot in self.slots:
      if slot.row == i and slot.col == j:
        return slot
    return None

  def rebuild_grid(self) -> list[list[str]]:
    new_grid = [row.copy() for row in self.grid]

    for slot in self.slots:
      char = slot.value if slot.value is not None else '?'
      new_grid[slot.row][slot.col] = char
      
    return new_grid
