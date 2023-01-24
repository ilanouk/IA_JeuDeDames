import tkinter as tk
 

# Création de la fenêtre principale (main window)
def fen():
    cell_size = 20
    board_size = 10 # ou 8 pour un échiquier
    canvas_size = cell_size * board_size
    
    colors = ["white", "black"]
    
    root = tk.Tk()
    
    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack()
    
    for x in range(board_size):
        for y in range(board_size):
            color = colors[(x + y) % 2]
            canvas.create_rectangle(
                y * cell_size,
                x * cell_size,
                y * cell_size + cell_size,
                x * cell_size + cell_size,
                fill=color, outline=color
            )
    
    root.mainloop()

fen()