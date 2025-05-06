import os

OUTPUT_PATH = "output"

def create_output_path() -> None:
  if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
    
    
def create_output_txt(file_name: str, data: str) -> None:
  file_path = os.path.join(OUTPUT_PATH, file_name)
  with open(file_path, 'w', encoding='utf-8') as f:
    f.write(data)