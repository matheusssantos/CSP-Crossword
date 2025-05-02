class Slot:
  def __init__(self, row: int, col: int, value: str):
    self.row = row
    self.col = col
    self.value = value
    
  def __repr__(self):
    return self.value



class Word:
  def __init__(self, slots: list[Slot]):
    self._letters: list[Slot] = slots
    self._content: str = ''
    self.length = len(slots)
    
  def __repr__(self):
    self._update_content()
    return self._content
  
  def _update_content(self) -> None:
    self._content = ''.join(slot.value or '?' for slot in self._letters)

  def get_content(self) -> str:
    self._update_content()
    return self._content



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




cw = Crossword("grids/grid-11x11-20W-83L-38B.txt")
cw.print_grid()
print()
cw.generate_slots()
cw.extract_words()

cw._get_slot(1 ,2).value = "A"
cw._get_slot(1 ,3).value = "L"
cw._get_slot(0 ,2).value = "P"

new_grid = cw.rebuild_grid()

for row in new_grid:
  print(''.join(row))