import tkinter as tk
from tkinter import ttk

#declair main parameters for canvases
TIME = 0
WIDTH = 540
w0 = 42
w1 = WIDTH - w0
AXIS_LINE_POS = w0 * 0.5 
TICK_INTERVAL = 50 



RADIUS_FOR_TEST = 8

#animation parameters
MOVE_STEP = 5
ANIMATION_DELAY = 120

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


def traj_points(x_final):
    #points in format points= [x1,y1,x2,y2,...,xn,yn]
    
    points = []

    for x in range(1,int(x_final)+1,5):
        points.append(x)
        points.append(450)
    # cnv.create_line(points,smooth = True,arrow = "last",fill = "grey",width = 2,tags = "straight_line")
    return points

def animate_ball_simple_with_line_update(cnv,ball):
    
    coords = cnv.coords(ball)
    x1, y1, x2, y2 = coords
    cnv.delete("straight_line")
    #creates arrow till the beginning of the bounding box
    cnv.move(ball, MOVE_STEP, 0)
    cnv.create_line(traj_points(x1+RADIUS_FOR_TEST),smooth = True,arrow = "last",fill = "grey",width = 2,tags= "straight_line")
    cnv.after(ANIMATION_DELAY,animate_ball_simple_with_line_update,cnv,ball)


frame = tk.Frame(master=root)
cnv_0_0 = tk.Canvas(master=frame, width=w0, height=w0, bg="ivory", highlightthickness=1) 
cnv_0_1 = tk.Canvas(master=frame, width=w1, height=w0, bg="ivory", highlightthickness=1)
cnv_0_2 = tk.Canvas(master=frame, width=w0, height=w1, bg="ivory", highlightthickness=1)
cnv_main = tk.Canvas(master=frame, width=w1, height=w1, bg="ivory", highlightthickness=1) 

cnv_0_0.create_text(w0 * 0.4, w0 * 0.8, text="y", fill="black", tags="y_label", font=("Arial", 10, "bold")) 
cnv_0_0.create_text(w0 * 0.8, w0 * 0.4, text="x", fill="black", tags="x_label", font=("Arial", 10, "bold"))

cnv_0_1.create_line(1, AXIS_LINE_POS, w1 - 10, AXIS_LINE_POS, fill="black", width=2, arrow="last", tags="x_axis_line")

cnv_0_2.create_line(AXIS_LINE_POS, 1, AXIS_LINE_POS, w1 - 10, fill="black", width=2, arrow="last", tags="y_axis_line")

frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5) 
cnv_0_0.grid(row=0, column=0)
cnv_0_1.grid(row=0, column=1)
cnv_0_2.grid(row=1, column=0)
cnv_main.grid(row=1, column=1)

draw_axes()

cnv_main.create_line(
    traj_points(50-RADIUS_FOR_TEST),
    smooth = True,
    arrow = "last",
    fill = "grey",
    width = 2,
    tags= "straight_line"
)  

ball= cnv_main.create_oval(50-RADIUS_FOR_TEST,450-RADIUS_FOR_TEST,50+RADIUS_FOR_TEST,450+RADIUS_FOR_TEST,fill="black")

animate_ball_simple_with_line_update(cnv_main,ball)



















root.mainloop()