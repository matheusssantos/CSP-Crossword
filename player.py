from crossword import Crossword
from utils import contains_num, logger_factory

LOG_PLAYER = logger_factory("PLAYER", 'cyan')

class Player:
  def __init__(self, crossword: Crossword, words: list[str]):
    LOG_PLAYER("Inicializando Player")
    self.palavras_slots = crossword.words # Lista de objetos Word a serem preenchidos
    self.palavras_disponiveis = words # Palavras da lista_palavras.txt
    self.palavras_usadas: list[str] = []
    
    LOG_PLAYER("Montando domínios iniciais")
    # Domínios iniciais: palavras válidas por tamanho e sem dígitos
    self.dominios: dict = {
      palavra_obj: [p for p in self.palavras_disponiveis if len(p) == palavra_obj.length and not contains_num(p)]
      for palavra_obj in self.palavras_slots
    }
    LOG_PLAYER("Setup concluído!")


  def grid_completa(self) -> bool:
    # Verifica se todas as palavras estão preenchidas
    return all(getattr(palavra_obj, '_content', '') != '' for palavra_obj in self.palavras_slots)


  def pontuacao_mrv(self, palavra_obj) -> int:
    # MRV: tamanho do domínio corrente
    LOG_PLAYER(f"Heurística MRV aplicada: Slot com menor domínio selecionado ({len(self.dominios[palavra_obj])} candidatos).")
    return len(self.dominios[palavra_obj])


  def contador_celulas_preenchidas(self, palavra_obj) -> int:
    # Degree alternativo: número de Slots já preenchidos
    num = sum(1 for cel in palavra_obj._letters if cel.value is not None)
    LOG_PLAYER(f"Heurística Degree aplicada: Slot com {num} células já preenchidas.")
    return num


  def ordenar_slots_por_heuristica(self) -> None:
    # Combina MRV + Degree
    self.palavras_slots.sort(
      key=lambda p_obj: (self.pontuacao_mrv(p_obj), -self.contador_celulas_preenchidas(p_obj))
    )


  def forwardtrack(self) -> bool:
    # Propaga consistência filtrando domínios por aceitação
    LOG_PLAYER("Executando forward checking...")
    for palavra_obj in self.palavras_slots:
      if getattr(palavra_obj, '_content', '') == '':
        novo_dominio = [p for p in self.dominios[palavra_obj] if palavra_obj.accept(p)]
        if not novo_dominio:
          return False
        self.dominios[palavra_obj] = novo_dominio
    return True


  def backtrack(self) -> bool:
    if self.grid_completa():
      LOG_PLAYER("Grade completa! Solução encontrada.")
      return True
    
    # Seleciona próximo slot (MRV + Degree)
    self.ordenar_slots_por_heuristica()
    proximo = next(p for p in self.palavras_slots if getattr(p, '_content', '') == '')
    
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

      if self.forwardtrack() and self.backtrack():
        return True
      
      self.palavras_usadas = estado_usadas
      self.dominios = estado_dominios

      for cel in proximo._letters:
        cel.value = None
      proximo._update_content()
      
    return False


  def resolve_grid(self) -> None:
    LOG_PLAYER("Iniciando resolução da grade...")
    self.backtrack()
    LOG_PLAYER("Processo de resolução finalizado.")