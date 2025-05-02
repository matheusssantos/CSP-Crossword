from utils import contains_num


class Player:
  def __init__(self, crossword: 'Crossword', words: list[str]):
    self.crossword: 'Crossword' = crossword
    self.slot_words = crossword.words
    self.words: list[str] = words
    self.words_used: list[str] = []
    self.words_trashed: list[str] = []

  def cw_completed(self):
    for word in self.slot_words:
      if '?' in str(word):
        return False

    return True

  # Heurísticas
  def heuristic_order_slots(self) -> None:
    self.slot_words = sorted(
      self.slot_words,
      key=lambda word: word.length,
      reverse=True
    )

  def heuristic_order_words(self) -> None:
    self.words = sorted(
      self.words,
      key=lambda word: word == word[0] * len(word)
    )

  # to-do: novas e melhores heuristicas e criar backtracking ou refinamento de domínios
  def solve(self) -> None:
    while not self.cw_completed():
      for word in self.slot_words:
        for word_txt in self.words:
          if word_txt not in self.words_used and word_txt not in self.words_trashed:
            if contains_num(word_txt):
              self.words_trashed.append(word_txt)

            else:
              try:
                word.assign(word_txt)

              except ValueError:
                continue

              else:
                # self.crossword.print_new_grid() #
                # print() #
                self.words_used.append(word_txt)
                break