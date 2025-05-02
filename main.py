from crossword import Crossword
from utils import Timer, load_word_list, contains_num

grids = [
  "11x11-20W-83L-38B",
  # "15x15-34W-169L-56B",
  # "25x25-88W-400L-225B",
]

words = load_word_list("lista_palavras.txt")
words_used = []
words_trashed = []

timer = Timer("Tempo de execução")
timer.start()

for grid in grids:
  print(grid)
  print("START:")

  cw = Crossword("grids/grid-" + grid + ".txt")
  cw.print_grid()
  print()

  for word in cw.words:
    # print(word) #
    for word_txt in words:
      if word_txt not in words_used and word_txt not in words_trashed:
        if contains_num(word_txt):
          words_trashed.append(word_txt)

        else:
          try:
            word.assign(word_txt)

          except ValueError:
            continue

          else:
            # print(word_txt) #
            # print() #
            # cw.print_new_grid() #
            # print('\n') #
            words_used.append(word_txt)
            break

  print("\nEND:")
  cw.print_new_grid()

timer.end()
timer.print_response()