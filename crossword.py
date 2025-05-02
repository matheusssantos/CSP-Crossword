from slot import Slot
from word import Word


def load_grid(path: str) -> list[list[str]]:
  with open(path, 'r') as f:
    return [list(line.strip()) for line in f if line.strip()]


class Crossword:
  def __init__(self, grid_file_path: str):
    self.grid: list[list[str]] = load_grid(grid_file_path)
    self.slots: list[Slot] = []
    self.words: list[Word] = []
    self.__generate_slots()
    self.__extract_words()

  def print_grid(self) -> None:
    for row in self.grid:
      print("".join(row))

  def _get_slot(self, i: int, j: int) -> Slot:
    for slot in self.slots:
      if slot.row == i and slot.col == j:
        return slot
    return None

  def __generate_slots(self) -> None:
    for i, row in enumerate(self.grid):
      for j, cell in enumerate(row):
        if cell == "?":
          slot = Slot(i, j, None)
          self.slots.append(slot)
          
  def __extract_words(self) -> None:
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
    rows = len(self.grid)
    for j in range(rows):
      current_slots = []
      for i in range(rows + 1):
        cell = self.grid[i][j] if i < rows else '.'
        if cell == '?':
          current_slots.append(self._get_slot(i, j))
        else:
          if len(current_slots) > 1:
            self.words.append(Word(current_slots))
          current_slots = []

  def __rebuild_grid(self) -> list[list[str]]:
    new_grid = [row.copy() for row in self.grid]

    for slot in self.slots:
      char = slot.value if slot.value is not None else '?'
      new_grid[slot.row][slot.col] = char
      
    return new_grid

  def print_new_grid(self) -> None:
    new_grid = self.__rebuild_grid()

    for row in new_grid:
      print("".join(row))