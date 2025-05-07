
from rembg import remove
from PIL import Image


def remove_bg(input_path, output_path):
    
    inp = Image.open(input_path)
    output = remove(inp)
    output.save(output_path)
    Image.open(output_path).show()
    
remove_bg("mike.jpg", "mike.png")