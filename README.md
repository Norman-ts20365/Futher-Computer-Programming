
# Python Epidemic Simulation

This project consists of 2 simulation models:

**1. Simulation based on population in a grid (which can be found in [modified_model](https://github.com/Robbie-Mackay/Further-computing-project/tree/main/modified_model)):**

    $ python model_runsim.py 

**2. Simulation based on population acting as particles (which can be found in [main](https://github.com/Robbie-Mackay/Further-computing-project)):**

    $ python simulation.py

### First model: model_runsim.py
This script can be found in this folder: [modified_model](https://github.com/Robbie-Mackay/Further-computing-project/tree/main/modified_model)

This script runs simulations of an epidemic (e.g. coronavirus) spreading
around people on a 2-dimensional grid. The script can be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is all done using the same simulation code which can also be imported
from this file and used in other ways.

The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    $ python model_runsim.py               # run simulation with default settings
    $ python model_runsim.py --cases=10    # have 10 initial cases
    $ python model_runsim.py --help        # show all command line options

It is also possible to create a video of the animation (if you install
ffmpeg):

    $ python model_runsim.py --file=simulation.mp4

NOTE: You need to install ffmpeg for the above to work. The ffmpeg program
must also be on PATH.


### Second model: simulation.py

This script runs simulations of an epidemic (e.g. coronavirus) spreading
around people represented by moving particles.

The command line interface to the script makes it possible to run different
simulations without needing to edit the code e.g.:

    # run simulation with default settings:
    
    $ python simulation.py
    
    # 200 population between the age of 40 to 49; have 20 initial cases:
    
    $ python simulation.py --population 200 --cases 20 --age_group 4 
    

The age group is divided into 5 groups and is listed below along with the range of age group they represent.

1 = 0 - 19  
2 = 20 -29  
3 = 30 - 39  
4 = 40 - 49  
5 = 50 - 100  



*Further computing project by Melvin, Mohammad, Norman, Robbie and Obiora*
