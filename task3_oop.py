import tkinter as tk
import math
import time

# declairing main parameters for canvases
WIDTH = 540
W0 = 42
W1 = WIDTH - W0
AXIS_LINE_POS = W0 * 0.5 
TICK_INTERVAL = 50 

# simulation parameters
G = 9.81              #ускорение свободного падения
RHO_MEDIUM_1 = 1.225  # density of env 1 - air
RHO_MEDIUM_2 = 1000.0 #density of env 2 - water
BOUNDARY_Y = 300      # y coord of boundary

FRAME_RATE_MS = 20   # in ms
SCALE_FACTOR = 1 # for more realistic animation 

class Particle:
    """Class describing one particle"""
    def __init__(self, cnv, x_init, y_init, radius, part_dens, Cd, color):
        """
        cnv: main canvas
        x_init,y_init: initial position
        radius: radius of a particle
        part_dens: particle's density
        Cd: coefficient of drag (коэффициент аэродинамического сопротивления) for sphere = 0.47
        color: color of a particle
        """
        self.canvas = cnv
        self.color = color

        # physical parameters of a paritcle
        self.r = radius
        self.rho_p = part_dens
        self.Cd = Cd
        self.m = (4/3) * math.pi * radius**3 * self.rho_p 
        self.A = math.pi * radius**2                     
        
        # particle state (coords and velocity)
        self.x = x_init
        self.y = y_init
        self.v_x = 0.0
        self.v_y = 0.0
        self.g = G

        # graphical implementation
        self.canvas_id = self.canvas.create_oval(
            x_init - radius, y_init - radius, 
            x_init + radius, y_init + radius, 
            fill=self.color, 
            tags="particle"
        )
        self.trail_points = [x_init,y_init] 

    def update_physics(self, dt, rho_medium):
        """
        Calculates new coords with rho in count
        :param dt: dt
        :param rho_medium: rho of current environment
        """
        #Fnet = Fd + Fg
        #Fnet = ma
        #Fg = mg
        #Fd = K (=1/2 * p *Cd* A) * |v|* v
        #v(x,(i+1)) = vi + ax *dt
        #v(y,(i+1)) = vi + ay *dt

        # Calculating Fd
        # |v|
        v_mag = math.sqrt(self.v_x**2 + self.v_y**2)
    
        # K
        K = 0.5 * rho_medium * self.Cd * self.A
        
        # Fd = - K * V^2
        if v_mag > 1e-6: # Избегаем деления на ноль / нестабильности
            F_d_x = -K * v_mag * self.v_x
            F_d_y = -K * v_mag * self.v_y
        else:
            F_d_x = 0
            F_d_y = 0

        F_net_x = F_d_x
        a_x = (F_net_x / self.m)* SCALE_FACTOR
        # Fnet = Fg +Fd
        F_net_y = (self.m * self.g) + F_d_y
        a_y = (F_net_y / self.m)* SCALE_FACTOR
        
        self.v_x += a_x * dt
        self.v_y += a_y * dt
        
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        
        if len(self.trail_points) == 0 or self.y != self.trail_points[-1] or self.x != self.trail_points[-2]:
             self.trail_points.extend([self.x, self.y])

    def draw(self):
        """updates the coords on main canvas"""
        self.canvas.coords(
            self.canvas_id, 
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r
        )
        
        if self.y > self.canvas.winfo_height() - self.r:
             self.y = self.canvas.winfo_height() - self.r
             self.v_y *= -0.5 

    def get_trajectory_points(self):
        if len(self.trail_points) >= 4:
            return self.trail_points[:-2]
        return []

class Simulation:

    def __init__(self, root):
        self.root = root
        self.root.geometry(f'{WIDTH + W0 + 10}x{WIDTH + W0 + 10}')
        self.root.resizable(False, False)

        # Фреймы и Canvas
        self.frame = tk.Frame(master=root)
        self.cnv_0_0 = tk.Canvas(master=self.frame, width=W0, height=W0, bg="ivory", highlightthickness=1) 
        self.cnv_0_1 = tk.Canvas(master=self.frame, width=W1, height=W0, bg="ivory", highlightthickness=1)
        self.cnv_0_2 = tk.Canvas(master=self.frame, width=W0, height=W1, bg="ivory", highlightthickness=1)
        self.cnv_main = tk.Canvas(master=self.frame, width=W1, height=W1, bg="ivory", highlightthickness=1) 

        self._init_layout()
        self._draw_axes()
        self._draw_boundary()

        self.last_time = time.time()
        
        self.particles = [
            Particle(self.cnv_main, 100, 50, 30, part_dens=2700, Cd=0.47, color="blue"), 
            Particle(self.cnv_main, 250, 50, 8, part_dens=2700, Cd=0.47, color="red"),
            Particle(self.cnv_main, 400, 50, 15, part_dens=2700, Cd=0.47, color="green") 
        ]
        
        # Запуск анимации
        self.animate()

    def _init_layout(self):
        self.frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5) 
        self.cnv_0_0.grid(row=0, column=0)
        self.cnv_0_1.grid(row=0, column=1)
        self.cnv_0_2.grid(row=1, column=0)
        self.cnv_main.grid(row=1, column=1)

        # axes graph
        self.cnv_0_0.create_text(W0 * 0.4, W0 * 0.8, text="y", fill="black", tags="y_label", font=("Arial", 10, "bold")) 
        self.cnv_0_0.create_text(W0 * 0.8, W0 * 0.4, text="x", fill="black", tags="x_label", font=("Arial", 10, "bold"))
        self.cnv_0_1.create_line(1, AXIS_LINE_POS, W1 - 10, AXIS_LINE_POS, fill="black", width=2, arrow="last", tags="x_axis_line")
        self.cnv_0_2.create_line(AXIS_LINE_POS, 1, AXIS_LINE_POS, W1 - 10, fill="black", width=2, arrow="last", tags="y_axis_line")

    def _draw_axes(self):
        self.cnv_0_1.delete("tick")
        self.cnv_0_2.delete("tick")

        limit = int(W1) 
        
        for px in range(TICK_INTERVAL, limit, TICK_INTERVAL):
            self.cnv_0_1.create_line(px, AXIS_LINE_POS - 5, px, AXIS_LINE_POS + 5, fill="black", tags="tick")
            self.cnv_0_1.create_text(px, AXIS_LINE_POS + 10, text=f"{px}", anchor="n", font=("Arial", 8), fill="black", tags="tick")

        for px in range(TICK_INTERVAL, limit, TICK_INTERVAL):
            self.cnv_0_2.create_line(AXIS_LINE_POS - 5, px, AXIS_LINE_POS +5, px, fill="black", tags="tick")
            
            self.cnv_0_2.create_text(
                AXIS_LINE_POS - 10, px-7, 
                text=f"{px}", 
                anchor="e", 
                font=("Arial", 8), 
                fill="black", 
                tags="tick",
                angle=90
            )
        
    def _draw_boundary(self):
        self.cnv_main.create_line(
            0, BOUNDARY_Y, W1, BOUNDARY_Y, 
            fill="blue", width=2, dash=(10, 5), tags="boundary"
        )
        self.cnv_main.create_text(10, BOUNDARY_Y + 15, text="Вода", anchor="w", fill="black")
        self.cnv_main.create_text(10, BOUNDARY_Y - 15, text="Воздух", anchor="w", fill="black")

    def animate(self):
        current_time = time.time()
        # differense in time
        dt = current_time - self.last_time
        self.last_time = current_time

        self.cnv_main.delete("trajectory")
        
        # updating all the particles at once
        for particle in self.particles:
            
            # check the environment
            rho = RHO_MEDIUM_1
            if particle.y > BOUNDARY_Y:
                rho = RHO_MEDIUM_2
                
            # physics update
            particle.update_physics(dt, rho)
            
            particle.draw()
            
            # traj draw
            points = particle.get_trajectory_points()
            if len(points) >= 4:
                 self.cnv_main.create_line(
                    points,
                    smooth=True,
                    fill=self.cnv_main.itemcget(particle.canvas_id, "fill"), 
                    width=3,
                    tags="trajectory"
                )

    
        self.root.after(FRAME_RATE_MS, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    app = Simulation(root)
    root.mainloop()