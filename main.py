from crossword import Crossword
from player import Player
from utils import Timer, load_word_list

grids = [
  "11x11-20W-83L-38B",
  "15x15-34W-169L-56B",
  "25x25-88W-400L-225B",
]

list_words = load_word_list("lista_palavras.txt")

timer = Timer("Tempo de execução")
timer.start()

for grid in grids:
  print(grid)
  print("START:")

  cw = Crossword("grids/grid-" + grid + ".txt")
  cw.print_grid()
  print()

  player = Player(cw, list_words)
  player.resolve_grid()

  print("\nEND:")
  cw.print_new_grid()

  print()

timer.end()
timer.print_response()