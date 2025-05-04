from utils import contains_num, is_repeated

class Player:
  def __init__(self, crossword: 'Crossword', words: list[str]):
    self.crossword = crossword
    self.slot_words = crossword.words
    self.words = words
    self.words_used: list[str] = []

  def cw_completed(self) -> bool:
    # Verifica se todos os slots foram preenchidos (sem '?')
    return all('?' not in repr(ws) for ws in self.slot_words)

  def pontuacao_mrv(self, ws) -> int:
    # MRV: número de candidatos válidos restantes
    return sum(
      1
      for w in self.words
      if len(w) == ws.length and w not in self.words_used and not contains_num(w)
      and ws.accept(w)
    )

  def prefilled_cells(self, ws) -> int:
    # Degree alternativo: conta células já preenchidas no slot
    return sum(1 for slot in ws._letters if slot.value is not None)

  def compute_letter_frequency(self) -> dict[str, int]:
    # Frequência de letras em palavras ainda não usadas
    freq: dict[str, int] = {}
    for w in self.words:
      if w not in self.words_used:
        for ch in w:
          freq[ch] = freq.get(ch, 0) + 1
    return freq

  def lcv_score(self, w: str, freq: dict[str, int]) -> int:
    # LCV aproximado: soma das frequências das letras
    return sum(freq.get(ch, 0) for ch in w)

  def word_penalty(self, w: str) -> int:
    # penalidade para números e repetições
    num_digits = sum(ch.isdigit() for ch in w)
    max_rep = max(w.count(ch) for ch in set(w)) - 1
    return num_digits + max_rep

  # Heurística combinada MRV + Degree
  def order_slots_heuristics(self) -> None:
    self.slot_words.sort(
      key=lambda ws: (self.pontuacao_mrv(ws), -self.prefilled_cells(ws))
    )

  # Heurística LCV + penalidade para ordenação de valores
  def order_words_heuristics(self, ws) -> list[str]:
    candidates = [w for w in self.words if len(w) == ws.length]
    freq = self.compute_letter_frequency()
    scored: list[tuple[int, int, str]] = []
    for w in candidates:
      if not ws.accept(w):
        continue
      lcv = self.lcv_score(w, freq)
      pen = self.word_penalty(w)
      scored.append((-lcv, pen, w))  # mais lcv (freq) e menos penalidade primeiro
    scored.sort(key=lambda x: (x[0], x[1]))
    return [w for (_, _, w) in scored]

  def backtrack(self):
    print("Nenhum valor encontrado, realizando backtracking.")
    pass  # to-do: implementar refinamento de domínios

  def solve(self) -> None:
    while not self.cw_completed():
      self.order_slots_heuristics()
      for ws in self.slot_words:
        if '?' not in repr(ws):
          continue
        ordered = self.order_words_heuristics(ws)
        assigned = False
        for w in ordered:
          if w in self.words_used:
            continue
          try:
            ws.assign(w)
          except ValueError:
            continue
          else:
            self.words_used.append(w)
            assigned = True
            break
        if not assigned:
          self.backtrack()
          return