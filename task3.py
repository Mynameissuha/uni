import tkinter as tk
from tkinter import ttk
#declair main parameters for canvases
WIDTH = 540
w0 = 42
w1 = WIDTH - w0
AXIS_LINE_POS = w0 * 0.5 
TICK_INTERVAL = 50 


#object parameters
RADIUS_FOR_TEST = 8

#animation parameters
MOVE_STEP = 5
ANIMATION_DELAY = 90

root = tk.Tk()
root.geometry('600x600')
root.resizable(False, False)

width0_var = tk.DoubleVar(value=w0)

def draw_axes():
    cnv_0_1.delete("tick")
    cnv_0_2.delete("tick")

    limit = int(w1) 
    
    for px in range(TICK_INTERVAL, limit, TICK_INTERVAL):
        cnv_0_1.create_line(px, AXIS_LINE_POS - 5, px, AXIS_LINE_POS + 5, fill="black", tags="tick")
        cnv_0_1.create_text(px, AXIS_LINE_POS + 10, text=f"{px}", anchor="n", font=("Arial", 8), fill="black", tags="tick")

    for px in range(TICK_INTERVAL, limit, TICK_INTERVAL):
        cnv_0_2.create_line(AXIS_LINE_POS - 5, px, AXIS_LINE_POS +5, px, fill="black", tags="tick")
        
        cnv_0_2.create_text(
            AXIS_LINE_POS - 10, px-7, 
            text=f"{px}", 
            anchor="e", 
            font=("Arial", 8), 
            fill="black", 
            tags="tick",
            angle=90
        )


def update_w0():
    global w0, w1, AXIS_LINE_POS
    
    try:
        new_w0 = width0_var.get()
    except:
        return 
    
    if not 10 < new_w0 < WIDTH - 10:
        return
        
    w0 = new_w0
    w1 = WIDTH - w0
    AXIS_LINE_POS = w0 * 0.5 
   
    cnv_0_0.config(width=w0, height=w0)
    cnv_0_1.config(width=w1, height=w0)
    cnv_0_2.config(width=w0, height=w1)
    cnv_main.config(width=w1, height=w1)
    
    cnv_0_1.coords("x_axis_line", 1, AXIS_LINE_POS, w1 - 10, AXIS_LINE_POS)
    cnv_0_2.coords("y_axis_line", AXIS_LINE_POS, 1, AXIS_LINE_POS, w1 - 10) 
    
    cnv_0_0.coords("x_label", w0 * 0.8, w0 * 0.4) 
    cnv_0_0.coords("y_label", w0 * 0.4, w0 * 0.8) 

    draw_axes()


def animate_ball_simple(cnv,ball):
    coords = cnv.coords(ball)
    x1, y1, x2, y2 = coords
    cnv.move(ball, MOVE_STEP, 0)
    cnv.after(ANIMATION_DELAY,animate_ball_simple,cnv,ball)


frame = tk.Frame(master=root)
cnv_0_0 = tk.Canvas(master=frame, width=w0, height=w0, bg="ivory", highlightthickness=1) 
cnv_0_1 = tk.Canvas(master=frame, width=w1, height=w0, bg="ivory", highlightthickness=1)
cnv_0_2 = tk.Canvas(master=frame, width=w0, height=w1, bg="ivory", highlightthickness=1)
cnv_main = tk.Canvas(master=frame, width=w1, height=w1, bg="ivory", highlightthickness=1) 

entry = ttk.Entry(root, textvariable=width0_var, width=8)
update_w0_button = tk.Button(root, text="Обновить w0", command=update_w0)

cnv_0_0.create_text(w0 * 0.4, w0 * 0.8, text="y", fill="black", tags="y_label", font=("Arial", 10, "bold")) 
cnv_0_0.create_text(w0 * 0.8, w0 * 0.4, text="x", fill="black", tags="x_label", font=("Arial", 10, "bold"))

cnv_0_1.create_line(1, AXIS_LINE_POS, w1 - 10, AXIS_LINE_POS, fill="black", width=2, arrow="last", tags="x_axis_line")

cnv_0_2.create_line(AXIS_LINE_POS, 1, AXIS_LINE_POS, w1 - 10, fill="black", width=2, arrow="last", tags="y_axis_line")

frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5) 
cnv_0_0.grid(row=0, column=0)
cnv_0_1.grid(row=0, column=1)
cnv_0_2.grid(row=1, column=0)
cnv_main.grid(row=1, column=1)

entry.grid(row=2, column=0, padx=0, pady=5, sticky='e')
update_w0_button.grid(row=2, column=1, padx=0, pady=5, sticky='w')

draw_axes()

ball= cnv_main.create_oval(50-RADIUS_FOR_TEST,450-RADIUS_FOR_TEST,50+RADIUS_FOR_TEST,450+RADIUS_FOR_TEST,fill="black")

animate_ball_simple(cnv_main,ball)
root.mainloop()