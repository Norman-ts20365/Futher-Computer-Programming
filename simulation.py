
#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from itertools import combinations
import random
import time 

def main(*args):
    """command line interface. There are inital values for the varibles that 
    will be able to effect the simulation. 
    These can all be edited as shown:
        
    $ python simulation.py                              ~Starts the simulation
    $ python simulation.py --population=200             ~Change to population size
    $ python simulation.py --file=example.mp4           ~ saves animation to file
    """
    
    
    parser = argparse.ArgumentParser(description='Create simulation and Animation of a pandemic')
    parser.add_argument('--population', metavar = 'N', type = int, default=200,
                        help = 'Total number of people')
    parser.add_argument('--radii',metavar ='N',type = float, default=0.01,
                        help = 'Size of the indiviual people')
    parser.add_argument('--cases', metavar = 'N', type = int, default = 4,
                        help = 'Number of people initally infected')
    parser.add_argument('--age_group',metavar = 'N', type = int, default = 1,
                        help = """group 1 = age 0 - 19
                                  group 2 = age 20 - 29
                                  group 3 = age 30 - 39
                                  group 4 = age 40 - 49
                                  group 5 = age 50 - 100 """)
    args = parser.parse_args(args)
    
    """Start simulation"""
    simulation = Simulation(args.population, args.radii,args.cases,
                            args.age_group,styles)

    simulation.do_animation()
    

class Particle:
    """Class for that produces the particles and their movements"""

    def __init__(self, x, y, vx, vy, radius, styles=None):
        """Initialize the particle's position, velocity, and radius."""

        self.r = np.array((x, y))
        self.v = np.array((vx, vy))
        self.radius = radius

        self.styles = styles



    @property
    def x(self):
        return self.r[0]
    @x.setter
    def x(self, position):
        self.r[0] = position
    @property
    def y(self):
        return self.r[1]
    @y.setter
    def y(self, position):
        self.r[1] = position
    @property
    def vx(self):
        return self.v[0]
    @vx.setter
    def vx(self, position):
        self.v[0] = position
    @property
    def vy(self):
        return self.v[1]
    @vy.setter
    def vy(self, position):
        self.v[1] = position

    def overlaps(self, other):
        """Does the circle of this Particle overlap that of other?"""

        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def draw(self, ax):
        """Add this Particle's Circle patch to the Matplotlib Axes ax."""

        circle = Circle(xy=self.r, radius=self.radius, **self.styles)
        ax.add_patch(circle)
        return circle

    def advance(self, dt):
        """Advance the Particle's position forward in time by dt."""

        self.r += self.v * dt

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
            
        if self.x + self.radius > 2:
            self.x = 2-self.radius
            self.vx = -self.vx
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
            
        if self.y + self.radius > 2:
            self.y = 2-self.radius
            self.vy = -self.vy

class Simulation:
    """A class Showing the movement of people, where a certain number of people "cases" are
    infected.
    """


    COLOURS = {
        'non-infected': 'blue',
        'infected': 'red',
        'recovered': 'green',
        'dead': 'black',
        'vaccinated':'purple',
    }

    def __init__(self, n, radius,cases,age_group,styles=None):
        """Initialize simulation for n people with the inital number of infected as the variable cases
        """
        self.day = 0
        self.cases = cases
        self.age_group = age_group
        self.init_people(n, radius, styles)
        self.vaccination_rate=0.01
        
    def init_people(self, n, radius, styles=None):
        """Initialize the n Particles of the simulation.
        Positions and velocities are chosen randomly
        """

        try:
            iterator = iter(radius)
            assert n == len(radius)
        except TypeError:
            def r_gen(n, radius):
                for i in range(n):
                    yield radius
            radius = r_gen(n, radius)

        self.infected = 0 
        self.n = n
        self.particles = []
        self.particles_age={}
        self.infected_particles = []
        self.recovered_particles = []
        self.dead_particles = []
        self.vaccinated_particles = []
        for i, rad in enumerate(radius):

            while True:

                x, y = np.random.uniform(0.0, 2.0, 2)

                vr = 1
                vphi = 2*np.pi * np.random.random()
                vx, vy = vr * np.cos(vphi), vr * np.sin(vphi)
                infected_style = {'edgecolor': 'C3', 'linewidth': 2, 'fill': 1}
                if self.infected < self.cases:
                    particle = Particle(x, y, vx, vy, rad, infected_style)
                    self.infected_particles.append(particle)
                    particle.time_infected = time.time()
                    self.infected += 1
                else:
                    particle = Particle(x, y, vx, vy, rad, styles)

                for p2 in self.particles:
                    if p2.overlaps(particle):
                        break
                else:
                    self.particles.append(particle)
                    break

    def people_interactions(self):
        """Detect and handle any collisions between People.
        When two People collide, they change their velcoities
        """

        def change_velocities(p1, p2):
            """
            Particles p1 and p2 have collided elastically: update their
            velocities.
            """

            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = p1.r, p2.r
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = p1.v, p2.v
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.v = u1
            p2.v = u2


        pairs = combinations(range(self.n), 2)
        for i,j in pairs:
            if self.particles[i].overlaps(self.particles[j]):
                change_velocities(self.particles[i], self.particles[j])
                if self.particles[i] in self.vaccinated_particles or  self .particles[j] in self.vaccinated_particles:
                    
                    continue 
                
                elif self.particles[i] in self.infected_particles and not self.particles[j] in self.recovered_particles and not self.particles[j] in self.dead_particles:
                    
                    self.particles[j].time_infected = time.time()
                    self.infected_particles.append(self.particles[j])
                    self.particles[j].styles = {'edgecolor': 'C3', 'linewidth': 2, 'fill': 1}

                elif self.particles[j] in self.infected_particles and not self.particles[i] in self.recovered_particles and not self.particles[i] in self.dead_particles:
                    
                    self.particles[i].time_infected = time.time() 
                    self.infected_particles.append(self.particles[i])
                    self.particles[i].styles = {'edgecolor': 'C3', 'linewidth': 2, 'fill': 1}
   
    
   
    def  duration_of_illness(self, age_group):
        """takes the age of the particles and sets the duration inwhich they are infected"""        
        
        if  age_group == 1:# between 0 and 19                 
            return 14 
            
        elif age_group ==2: # between 20 and 29          
            return 14
                    
        elif age_group == 3 :#between 30 and 39                    
            return 14
               
        elif age_group == 4 :#between 40 and 49         
            return 16
                     
        elif age_group== 5: #between 50 and 100     
            return 19 
          
    

    def age_setter(self):
        """Function that sets the age each indiviual particle"""
        
        for i in self.particles:
            Random=random.randint(0,100)
            if Random<19:
                self.particles_age[i]=random.randint(0,16)
                
            elif 19<=Random<82:
                self.particles_age[i]=random.randint(16,65)
                
            elif 82<Random:
                self.particles_age[i]=random.randint(65,100)
    
    
    def recovery_death(self):
        """Function that kills or recovers an infected particle"""
        
        for i in self.infected_particles:
            if time.time() - i.time_infected > Simulation.duration_of_illness('',1):
           
                chance = random.randint(1,10)
                
                if chance == 1:
                    i.styles = {'edgecolor': '0', 'linewidth': 2, 'fill': 1}
                    
                    self.infected_particles.remove(i)
                    self.dead_particles.append(i)
                else:
                    i.styles = {'edgecolor': 'C2', 'linewidth': 2, 'fill': 1}
                   
                    self.infected_particles.remove(i)
                    self.recovered_particles.append(i)
                        
    
    def vaccine(self,vaccination_rate):
        """Vaccinates people that are non-infected such that they are unable to be infected""" 
        
        chance_above_50=85
        chance_below_50=100-chance_above_50
        for i in self.particles:
            if self.day > 50: 
                
                if ((i not in self.infected_particles)
                    and (i not in self.dead_particles)
                    and (i not in self.vaccinated_particles)
                    and (i not in self.recovered_particles)):

                    chance= random.randint(0,100)
                    
                    if chance<=vaccination_rate:

                        if self.particles_age[i]>=50:
                            
                            if random.randint(0,100) <= chance_above_50:
                               
                                i.styles = {'edgecolor': 'C4', 'linewidth': 2, 'fill': 1}
                                self.vaccinated_particles.append(i)

                               
                        elif 10<= self.particles_age[i]<50:
                            
                            if random.randint(0,100)<=chance_below_50:
                                
                                i.styles = {'edgecolor': 'C4', 'linewidth': 2, 'fill': 1}
                                self.vaccinated_particles.append(i)
        return self.vaccinated_particles
                
                  

    def advance_animation(self, dt):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.particles):
            p.advance(dt)
            self.circles[i].center = p.r
            
        self.people_interactions()
        self.recovery_death()
        self.age_setter()
        self.duration_of_illness(self.age_group)
        self.vaccine(self.vaccination_rate)
        return self.circles

    def advance(self, dt):
        """Advance the animation by dt."""
        
        for i, p in enumerate(self.particles):
            p.advance(dt)
        self.people_interactions()


    
    def count_states(self):
        """counts the number of particles with each state"""
        self.count = {}
        
        self.num_infected = len(self.infected_particles)
        self.num_recovered = len(self.recovered_particles)
        self.num_dead = len(self.dead_particles)
        self.num_vaccinated = len(self.vaccinated_particles)
        self.num_noninfected = len(self.particles) - self.num_infected - self.num_recovered - self.num_dead - self.num_vaccinated
        
        self.count["non-infected"] = self.num_noninfected
        self.count["infected"] = self.num_infected
        self.count["recovered"] = self.num_recovered
        self.count["dead"] = self.num_dead
        self.count["vaccinated"] = self.num_vaccinated
        return self.count
    
    

    
    def do_animation(self):
        """Set up and carry out the animation of the molecular dynamics.
        To save the animation as a MP4 movie, set save=True.
        """
        
        fig,self.axs = plt.subplots(1,2,figsize=(10,5))

                                      
        anim = animation.FuncAnimation(fig,self.update,init_func = self.init, frames=100,interval = 2,blit=False )
        plt.draw()
        
        plt.show()


    def grid_init(self):
        """Initialize the animation of the people onto the figure"""
        
        self.axs[0].xaxis.set_ticks([])
        self.axs[0].yaxis.set_ticks([])
        self.axs[0].set(xlim=(0,2),ylim=(0,2))
        
        for s in ['top','bottom','left','right']:
            self.axs[0].spines[s].set_linewidth(2)
        self.axs[0].set_aspect('equal', 'box')
        
        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.axs[0]))
        return self.circles


    def animate(self, i):
        """updates the animation of the people """

        self.advance_animation(i)
        return self.circles
    
    def init(self):
        """combines all the initiation functions into one function"""
        
        actors = []
        actors+= self.grid_init()
        actors+= self.line_init()
        return actors
    
    def update(self,frames):
        """combines all the update functions into one function"""
        
        actors = []
        actors += self.animate(0.01)
        actors += self.line_update(frames)
        return actors
    
   
    def line_init(self): 
        """initiates the line graph onto the figure"""
        
        self.xvalues = [self.day]
        self.yvalues = {status : [] for status in self.COLOURS}
        self.lines = {}
        self.count_states()

        self.axs[1].set_xlabel('days')
        self.axs[1].set_ylabel('number of people', rotation=90)
        
        for status,value in self.count.items():
                self.yvalues[status] = self.yvalues.get(status,[]) + [value]
            
        for status,colour in self.COLOURS.items():
            
            [line] = self.axs[1].plot(self.xvalues,self.yvalues[status],color=colour, label=status,linewidth =2,)
            self.lines[status] = line
        
        handles = [self.lines["non-infected"],self.lines["infected"],self.lines["recovered"],self.lines["dead"],self.lines["vaccinated"]]
        labels = ["non-infected","infected","recovered","dead","vaccinated"]
        self.axs[1].legend(handles,labels,loc="upper right")
        
        return self.lines
            
        
    
    def line_update(self,frames):
        """updates the line graph """
        
        self.count_states()
        self.day+=1
        self.xvalues.append(self.day)
        
        for status,value in self.count.items():
                self.yvalues[status] = self.yvalues.get(status,[]) + [value]
                
        for status,colour in self.COLOURS.items():
                    [line] = self.axs[1].plot(self.xvalues,self.yvalues[status],color=colour,linewidth =2,)
                    self.lines[status] = line        
        return self.lines
    
    
    


if __name__ == '__main__':
    styles = {'edgecolor': 'C0', 'linewidth': 2, 'fill': 1}
    import sys
    main(*sys.argv[1:])

