from crossword import Crossword
from utils import Timer

def load_word_list(path: str) -> list[str]:
  with open(path, 'r', encoding='utf-8') as f:
    return [line.strip().upper() for line in f if line.strip()]


timer = Timer("Tempo de execução")

timer.start()

cw = Crossword("grids/grid-11x11-20W-83L-38B.txt")
print("START:")
cw.print_grid()
cw.generate_slots()
cw.extract_words()

words = load_word_list("lista_palavras.txt")

timer.end()
timer.print_response()