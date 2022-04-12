import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from itertools import islice


class Animation:
    """Create an animation of the epidemic.

    This creates a plot figure with two subplots:

        A colormap showing the status of the people.
        A line plot showing how many people are in each status.

    The resulting animation can either be shown on screen (with show()) or can
    be saved to a file (with save()).

    Example
    =======

    Create a simulation and animate it for 365 days showing the animation on
    screen:

    >>> sim = Simulation(100, 100, recovery=0.1, infection=0.2, death=0.05)
    >>> sim.infect_randomly(3)  # infect three people (chosen randomly)
    >>> anim = Animation(simulation, 365)
    >>> animshow()

    """

    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration

        self.figure = plt.figure(figsize=(8, 8))
        self.axes_grid = self.figure.add_subplot(2, 1, 1)
        self.axes_grid.title.set_text('Epidemic Simulation')
        self.axes_line = self.figure.add_subplot(2, 1, 2)

        self.gridanimation = GridAnimation(self.axes_grid, self.simulation)
        self.lineanimation = LineAnimation(self.axes_line, self.simulation, duration)

    def show(self):
        """Run the animation on screen"""
        
        animation = FuncAnimation(self.figure, self.update, frames=range(100),
                init_func = self.init, blit=True, interval=200)
        plt.show()

    def save(self, filename):
        """Run the animation and save to a video"""

        # NOTE: needs ffmpeg installed and on PATH
        animation = FuncAnimation(self.figure, self.update, frames=range(365),
                init_func = self.init, blit=True, interval=300)
        animation.save(filename, fps=10, extra_args=['-vcodec', 'libx264'])


    def init(self):
        """Initialise the animation (called by FuncAnimation)"""
        # We could generalise this to a loop and then it would work for any
        # numer of *animation objects.
        actors = []
        actors += self.gridanimation.init()
        actors += self.lineanimation.init()
        return actors

    def update(self, framenumber):
        """Update the animation (called by FuncAnimation)"""
        self.simulation.update()
        actors = []
        actors += self.gridanimation.update(framenumber)
        actors += self.lineanimation.update(framenumber)
        return actors


class GridAnimation:
    """Animate a grid showing status of people at each position"""

    def __init__(self, axes, simulation):
        self.axes = axes
        self.simulation = simulation
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image = self.axes.imshow(rgb_matrix)
        self.axes.set_xticks([])
        self.axes.set_yticks([])

    def init(self):
        return self.update(0)

    def update(self, framenum):
        day = framenum
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image.set_array(rgb_matrix)
        return [self.image]

# Get value of args.population from modelrunsim.py
def get_ylim(num):
    global ylim_value
    ylim_value = num
    

class LineAnimation:
    """Animate a line series showing numbers of people in each status"""

    def __init__(self, axes, simulation, duration):
        self.axes = axes
        self.simulation = simulation
        self.duration = duration
        self.xdata = []
        self.ydata = {status: [] for status in islice(simulation.STATUSES,1,None)}
        self.line_mpl = {}
        for status, colour in islice(simulation.COLOURMAP.items(),1,None):
            [line] = self.axes.plot([], [], color=colour, label=status, linewidth=2)
            self.line_mpl[status] = line
        
        plt.axhline(y = self.simulation.healthcare_capacity,
                    color = 'violet', linestyle = 'dashed', label='healthcare capacity')
        
        plt.axhline(y = self.simulation.lockdown_when_cases,
                    color = 'c', linestyle = 'dashed', label='lockdown') 
        
        self.axes.legend(prop={'size':'x-small'}, bbox_to_anchor=(1, 1.35), loc='upper right', )
        self.axes.set_xlabel('days')
        self.axes.set_ylabel('Number of people', rotation=90)
    
    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, ylim_value]) #ylim_value is population
        return []

    def update(self, framenum):
        status_counts = self.simulation.get_counts_status()
        self.xdata.append(len(self.xdata))
        for status, count in islice(status_counts.items(),1, None): #avoid plotting "space" on graph
            self.ydata[status].append(count)
            self.line_mpl[status].set_data(self.xdata, self.ydata[status])
        return list(self.line_mpl.values())