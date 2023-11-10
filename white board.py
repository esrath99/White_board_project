import tkinter as tk
from tkinter.colorchooser import askcolor

def start_drawing(event):
    global is_drawing, prev_x, prev_y
    if not is_selecting:  # Only start drawing when not in select mode
        is_drawing = True
        prev_x, prev_y = event.x, event.y

def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)
        prev_x, prev_y = current_x, current_y

def stop_drawing(event):
    global is_drawing
    is_drawing = False

def toggle_select_mode():
    global is_selecting, is_drawing
    is_selecting = not is_selecting
    if is_selecting:
        is_drawing = False
        selected_items.clear()
    else:
        is_drawing = True


def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color

def change_line_width(value):
    global line_width
    line_width = int(value)

def select(event):    
    global select_start_x, select_start_y, select_rect
    select_start_x, select_start_y = event.x, event.y
    select_rect = None

def draw_selection(event):
    global select_rect
    if is_selecting:
        current_x, current_y = event.x, event.y
        if select_rect:
            canvas.delete(select_rect)
        select_rect = canvas.create_rectangle(select_start_x, select_start_y, current_x, current_y, outline='blue', dash=(4,))

def end_selection(event):
    global select_rect, selected_items
    current_x, current_y = event.x, event.y
    if select_rect:
        canvas.delete(select_rect)
    if is_selecting:
        items = canvas.find_enclosed(select_start_x, select_start_y, current_x, current_y)
        selected_items.extend(items)

def copy_selection(event=None):  # Added event parameter to make it a function that can be bound to Ctrl+C
    global copied_items
    copied_items = selected_items

def paste_selection(event=None):  # Added event parameter to make it a function that can be bound to Ctrl+V
    x_offset, y_offset = 20, 20  # Adjust the paste position
    for item in copied_items:
        item_type = canvas.type(item)
        if item_type == 'line':
            coords = canvas.coords(item)
            new_coords = [x + x_offset if i % 2 == 0 else x + y_offset for i, x in enumerate(coords)]
            canvas.create_line(new_coords, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)

def delete_selection(event=None):  
    for item in selected_items:
        canvas.delete(item)


def delete_selections(event=None):  
    if event.keysym == 'Delete' and event.state & 0x0080:
        for item in selected_items:
            canvas.delete(item)



root = tk.Tk()
root.title("Whiteboard App")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

is_drawing = False
is_selecting = False
drawing_color = "black"
line_width = 2
select_rect = None  # Declare select_rect as a global variable

selected_items = []

root.geometry("800x600")

controls_frame = tk.Frame(root)
controls_frame.pack(side="top", fill="x")

color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color)
clear_button = tk.Button(controls_frame, text="Clear Canvas", command=lambda: canvas.delete("all"))
clear_selection = tk.Button(controls_frame, text="Clear Selection", command=delete_selection)


color_button.pack(side="left", padx=5, pady=5)
clear_button.pack(side="left", padx=5, pady=5)
clear_selection.pack(side="left", padx=5, pady=5)


line_width_label = tk.Label(controls_frame, text="Line Width:")
line_width_label.pack(side="left", padx=5, pady=5)

line_width_slider = tk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val))
line_width_slider.set(line_width)
line_width_slider.pack(side="left", padx=5, pady=5)

select_button = tk.Button(controls_frame, text="Select", command=toggle_select_mode)
select_button.pack(side="left", padx=5, pady=5)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<Button-1>", select, add=True)
canvas.bind("<B1-Motion>", draw_selection, add=True)
canvas.bind("<ButtonRelease-1>", end_selection, add=True)


# Keyboard shortcuts
root.bind("<Command-c>", copy_selection)  # Ctrl+C to copy
root.bind("<Command-v>", paste_selection)  # Ctrl+V to paste
# root.bind("<Key-Delete>", delete_selection)     # Delete key to delete
root.bind("<Command-Delete>", delete_selections)

root.mainloop()
