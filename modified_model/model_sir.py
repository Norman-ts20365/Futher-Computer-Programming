import numpy as np
from numpy.random import random, randint
import random
from itertools import islice


class Simulation:
    # Spaces and status codes to store in the numpy array representing the state.
    SPACE = 0
    SUSCEPTIBLE = 1
    INFECTED = 2
    RECOVERED = 3
    DEAD = 4

    STATUSES = {
        'space': SPACE,
        'susceptible': SUSCEPTIBLE,
        'infected': INFECTED,
        'recovered': RECOVERED,
        'dead': DEAD,
        
    }
    COLOURMAP = {
        'space': 'gray',
        'susceptible': 'green',
        'infected': 'red',
        'recovered': 'blue',
        'dead': 'black',
        
    }
    COLOURMAP_RGB = {
        'gray': (211,211,211),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        
    }
    
    def __init__(self, width, height, recovery, infection, death, 
                 capacity, lockdown, infectionCap, deathCap,):
        # Basic simulation parameters:
        self.day = 0
        self.infection_probability = 0
        self.death_probability = 0
        self.width = width
        self.height = height
        self.recovery_probability = recovery
        self.infection_probability_healthcare = infection
        self.death_probability_healthcare = death
        
        # Additional features:
        self.healthcare_capacity = capacity
        self.lockdown_when_cases = lockdown   
        
        # SIR probabilites when healthcare capacity is reached:
        self.infection_probability_healthCap = infectionCap
        self.death_probability_healthCap = deathCap
        

        
        # Initial state (just empty spaces)
        self.state = np.zeros((width, height), int)
        self.state[:, :] = self.SPACE
        
    def population(self, num):
        """Place number of people randomly in the grid of empty spaces"""
        people = []
        
        num_people = 0
        
        while num_people < num:
            i = randint(self.width)
            j = randint(self.height)
            
            if (i,j) not in people:
                people.append((i,j))
                num_people += 1
                
                self.state[i, j] = self.SUSCEPTIBLE
                
    
    def infect_randomly(self,num):
        """Choose num people randomly and make them infected"""
        # Choose a random x, y coordinate and make that person infected
        # Without repeating
        # Num is number of people infected
        row = random.sample(range(self.width), num)
        column = random.sample(range(self.height), num)
        
        for i in row:
            j = random.sample(range(len(column)), 1)[0]
            self.state[i,j] = self.INFECTED
                
    
    def update(self):
        """Advance the simulation by one day"""
        # Use a copy of the old state to store the new state so that e.g. if
        # someone recovers but was infected yesterday their neighbours might
        # still become infected today.
        old_state = self.state
        new_state = old_state.copy()
        
        for i in range(self.width):
            for j in range(self.height):
                new_state[i, j] = self.get_new_status(old_state, i, j)
        self.state = new_state
        
        
        status_infected = self.get_counts_status()
        for infected, count in islice(status_infected.items(),2,3):
            
            # Implement lockdown when cases is above certain value.
            # If user state args.lockdown = 0, means no lockdown will be implemented
            if count < self.lockdown_when_cases or self.lockdown_when_cases == 0:
                # Shuffle the gird to represent movement when no lockdown.
                for n in range(self.width):
                    np.random.shuffle(self.state[n])
                    np.random.shuffle(self.state)
                    
            # Change infection and death probabilities when healthcare
            # capacity is reached.
            # If user state args.capacity = 0, means infinite healthcare capacity
            if self.healthcare_capacity != 0:
                if count > self.healthcare_capacity:
                    if self.death_probability_healthCap: 
                        self.death_probability = self.death_probability_healthCap
                        self.infection_probability = self.infection_probability_healthCap 

            if count < self.healthcare_capacity or self.healthcare_capacity == 0:
                if self.death_probability_healthCap: 
                    self.death_probability = self.death_probability_healthcare
                    self.infection_probability = self.infection_probability_healthcare
                    
        self.day += 1
    
    
    def get_new_status(self, state, i, j):
        status = state[i, j]
        
        # Update infected person
        if status == self.INFECTED:
            if self.recovery_probability > random.random():
                return self.RECOVERED
            elif self.death_probability > random.random():
                return self.DEAD

        # Update susceptible person
        elif status == self.SUSCEPTIBLE:
            num = self.num_infected_around(state, i, j)
            if num * self.infection_probability > random.random():
                return self.INFECTED

        # Return the old status (e.g. DEAD/RECOVERED)
        return status


    def num_infected_around(self, state, i, j):
        """Count the number of infected people around person i, j"""

        # Need to be careful about people at the edge of the grid.
        # ivals and jvals are the coordinates of neighbours around i, j
        ivals = range(max(i-1, 0), min(i+2, self.width))
        jvals = range(max(j-1, 0), min(j+2, self.height))
        number = 0
        for ip in ivals:
            for jp in jvals:
                # Don't count self as a neighbour
                if (ip, jp) != (i, j):
                    if state[ip, jp] == self.INFECTED:
                        number += 1

        return number


    def get_counts_status(self):
        """Dict giving number of people in each status"""

        simgrid = self.state
        
        counts = {}
        
        for status, statusnum in self.STATUSES.items():
            count = np.count_nonzero(simgrid == statusnum)
            counts[status] = count
            
        return counts


    def get_rgb_matrix(self):
        """RGB matrix representing the statuses of the people in the grid

        This represents the state as an RGB (colour) matrix using the
        coloursceheme set in the class variables COLOURMAP and COLOURMAP_RGB.
        The resulting matrix is suitable to be used with e.g. matplotlib's
        imshow function.
        """
        rgb_matrix = np.zeros((self.width, self.height, 3), int)
        for status, statusnum in self.STATUSES.items():
            colour_name = self.COLOURMAP[status] #eg. gray
            colour_rgb = self.COLOURMAP_RGB[colour_name] #eg. (211,211,211)
            rgb_matrix[self.state == statusnum] = colour_rgb
            
        return rgb_matrix