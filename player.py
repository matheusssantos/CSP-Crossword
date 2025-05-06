from crossword import Crossword
from utils import contains_num

class Player:
  def __init__(self, crossword: Crossword, words: list[str]):
    self.palavras_slots = crossword.words # Lista de objetos Word a serem preenchidos
    self.palavras_disponiveis = words # Palavras da lista_palavras.txt
    self.palavras_usadas: list[str] = []
    # Domínios iniciais: palavras válidas por tamanho e sem dígitos
    self.dominios: dict = {
      palavra_obj: [p for p in self.palavras_disponiveis
                    if len(p) == palavra_obj.length and not contains_num(p)]
      for palavra_obj in self.palavras_slots
    }

  def grid_completa(self) -> bool:
    # Verifica se todas as palavras estão preenchidas
    return all(getattr(palavra_obj, '_content', '') != '' for palavra_obj in self.palavras_slots)

  def pontuacao_mrv(self, palavra_obj) -> int:
    # MRV: tamanho do domínio corrente
    return len(self.dominios[palavra_obj])

  def contador_celulas_preenchidas(self, palavra_obj) -> int:
    # Degree alternativo: número de Slots já preenchidos
    return sum(1 for cel in palavra_obj._letters if cel.value is not None)

  def ordenar_slots_por_heuristica(self) -> None:
    # Combina MRV + Degree
    self.palavras_slots.sort(
      key=lambda p_obj: (self.pontuacao_mrv(p_obj), -self.contador_celulas_preenchidas(p_obj))
    )

  def ordenar_palavras_por_heuristica(self, palavra_obj) -> list[str]:
    # LCV + penalidade: calcular frequência de letras nos domínios
    frequencia: dict[str, int] = {}
    for dominio in self.dominios.values():
      for p in dominio:
        for ch in p:
          frequencia[ch] = frequencia.get(ch, 0) + 1
    lista_valores: list[tuple[int, int, str]] = []
    for p in self.dominios[palavra_obj]:
      lcv = sum(frequencia.get(ch, 0) for ch in p)
      penalidade = sum(ch.isdigit() for ch in p) + (max(p.count(c) for c in set(p)) - 1)
      lista_valores.append((-lcv, penalidade, p))
    lista_valores.sort(key=lambda item: (item[0], item[1]))
    return [p for (_, _, p) in lista_valores]

  def forwardtrack(self) -> bool:
    # Propaga consistência filtrando domínios por aceitação
    for palavra_obj in self.palavras_slots:
      if getattr(palavra_obj, '_content', '') == '':
        novo_dominio = [p for p in self.dominios[palavra_obj] if palavra_obj.accept(p)]
        if not novo_dominio:
          return False
        self.dominios[palavra_obj] = novo_dominio
    return True

  def backtrack(self) -> bool:
    if self.grid_completa():
      return True
    # Seleciona próximo slot (MRV + Degree)
    self.ordenar_slots_por_heuristica()
    proximo = next(p for p in self.palavras_slots
                   if getattr(p, '_content', '') == '')
    # Tenta valores do domínio
    for valor in list(self.dominios[proximo]):
      if valor in self.palavras_usadas:
        continue
      if not proximo.accept(valor):
        continue
      # Salva estado atual
      estado_usadas = list(self.palavras_usadas)
      estado_dominios = {k: list(v) for k, v in self.dominios.items()}
      # Atribui valor
      proximo.assign(valor)
      self.palavras_usadas.append(valor)
      # Propaga e recursa
      if self.forwardtrack() and self.backtrack():
        return True
      # Restaura estado
      self.palavras_usadas = estado_usadas
      self.dominios = estado_dominios
      # Limpa atribuição do slot
      for cel in proximo._letters:
        cel.value = None
      proximo._update_content()
    return False

  def resolve_grid(self) -> None:
    self.backtrack()