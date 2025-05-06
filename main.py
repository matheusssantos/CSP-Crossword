from crossword import Crossword
from player import Player
from utils import Timer, load_word_list
from utils import LOG_SYSTEM

LOG_SYSTEM('Iniciando sistema...')

GRIDS = [
  "11x11-20W-83L-38B",
  "15x15-34W-169L-56B",
  # "25x25-88W-400L-225B",
]

LIST_WORDS = load_word_list("lista_palavras.txt")
LOG_SYSTEM('Lista de palavras carregada.')

timer = Timer("Tempo de execução geral")
timer.start()

for grid in GRIDS:
  grid_size = grid.split('-')[0]
  LOG_SYSTEM(f'Inciando resolução para Grid {grid_size}')
  
  grid_timer = Timer(f"Tempo de execução para Grid {grid_size}")
  grid_timer.start()

  cw = Crossword("grids/grid-" + grid + ".txt")

  player = Player(cw, LIST_WORDS)
  player.resolve_grid()

  grid_timer.end()
  grid_timer.print_response()

timer.end()
timer.print_response()