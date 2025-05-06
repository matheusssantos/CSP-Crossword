from crossword import Crossword
from player import Player
from utils import Timer, load_word_list, LOG_SYSTEM, LOG_HISTORY_LIST
from file_manager import create_output_path, create_output_txt

def save_output_file(grid_name: str, grid: list[list[str]]):
  output_data = ''
  for row in grid:
    output_data += "".join(row) + '\n'
  
  create_output_txt(f"grid-{grid_name}.output.txt", output_data)


def save_log_file(grid_name: str):
  output_data = ''
  for entry in LOG_HISTORY_LIST:
    output_data += entry + "\n"
  
  create_output_txt(f"{grid_name}.log.txt", output_data)
  LOG_HISTORY_LIST.clear()
  

LOG_SYSTEM('Iniciando sistema...', add_to_history=False)

GRIDS = [
  "11x11-20W-83L-38B",
  "15x15-34W-169L-56B",
  "25x25-88W-400L-225B",
]

create_output_path()

LIST_WORDS = load_word_list("lista_palavras.txt")
LOG_SYSTEM('Lista de palavras carregada.', add_to_history=False)

timer = Timer("Tempo de execução geral")
timer.start()

for grid_name in GRIDS:
  grid_size = grid_name.split('-')[0]
  LOG_SYSTEM(f'Inciando resolução para Grid {grid_size}')
  
  grid_timer = Timer(f"Tempo de execução para Grid {grid_size}")
  grid_timer.start()

  cw = Crossword("grids/grid-" + grid_name + ".txt")
  cw.print_grid()

  player = Player(cw, LIST_WORDS)
  player.resolve_grid()
  
  resolved_grid = cw.get_resolved_grid()
  save_output_file(grid_name, resolved_grid)

  grid_timer.end()
  grid_timer.print_response()
  save_log_file(grid_name)
  

timer.end()
timer.print_response()
