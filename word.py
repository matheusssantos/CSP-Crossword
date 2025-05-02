from slot import Slot


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

  def accept(self, word: str) -> bool:
    if len(word) != len(self._letters):
      return False
    for i, slot in enumerate(self._letters):
      if slot.value is not None and slot.value != word[i]:
        return False
    return True
  
  def assign(self, word: str) -> None:
    if not self.accept(word):
      raise ValueError(f"Palavra '{word}' não pode ser atribuída a este slot.")
    for i, slot in enumerate(self._letters):
      slot.value = word[i]
    self._update_content()
