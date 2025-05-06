from slot import Slot
from word import Word
from utils import logger_factory

LOG_CROSSWORD = logger_factory("CROSSWORD", 'yellow')


def load_grid(path: str) -> list[list[str]]:
  with open(path, 'r') as f:
    return [list(line.strip()) for line in f if line.strip()]


class Crossword:
  def __init__(self, grid_file_path: str):
    LOG_CROSSWORD(f"Crossword {grid_file_path.split('-')[1]} selecionado.")
    LOG_CROSSWORD("Carregando arquivo...")
    self.grid: list[list[str]] = load_grid(grid_file_path)
    self.slots: list[Slot] = []
    self.words: list[Word] = []
    LOG_CROSSWORD("Gerando Slots")
    self.__generate_slots()
    LOG_CROSSWORD("Extraindo Words")
    self.__extract_words()
    LOG_CROSSWORD("Setup concluído!")

  def print_grid(self) -> None:
    data = 'Grid para resolver:'
    for row in self.grid:
      data += '\n' + "".join(row)
    LOG_CROSSWORD(data)

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
    
    LOG_CROSSWORD("Grid reconstruida com sucesso")
    return new_grid

  def get_resolved_grid(self):
    new_grid = self.__rebuild_grid()
    
    data = 'Grid resolvida:'
    for row in new_grid:
      data += '\n' + "".join(row)
    LOG_CROSSWORD(data)
    
    return new_grid
  