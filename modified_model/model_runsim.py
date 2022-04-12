import argparse

import matplotlib.pyplot as plt

from model_sir import Simulation
from model_animation import Animation, LineAnimation
from model_plot import plot_simulation

from model_animation import get_ylim


def main(*args):
    """Command line entry point.

    $ python runsim_model.py                        # show animation on screen
    $ python runsim_model.py --file=video.mp4       # save animation to video
    $ python runsim_model.py --plot                 # show plot on screen
    $ python runsim_model.py --plot --file=plot.pdf # save plot to pdf

    """
    #
    # Use argparse to handle parsing the command line arguments.
    #
    parser = argparse.ArgumentParser(description='Animate an epidemic')
    parser.add_argument('--size', metavar='N', type=int, default=100,
                        help='Use a N x N simulation grid')
    parser.add_argument('--duration', metavar='T', type=int, default=365,
                        help='Simulate for T days')
    parser.add_argument('--recovery', metavar='P', type=float, default=0.02,
                        help='Probability of recovery (per day)')
    parser.add_argument('--infection', metavar='P', type=float, default=0.03,
                        help='Probability of infecting a neighbour (per day)')
    parser.add_argument('--death', metavar='P', type=float, default=0.002,
                        help='Probability of dying when infected (per day)')
    parser.add_argument('--deathCap', metavar='P', type=float, default=0.005,
                        help='Probability of dying when healthcare capacity is reached')
    parser.add_argument('--infectionCap', metavar='P', type=float, default=0.05,
                        help='Probability of infection when healthcare capacity is reached')
    parser.add_argument('--population', metavar='N', type=int, default=6000,
                        help='The size of the population')
    parser.add_argument('--cases', metavar='N', type=int, default=2,
                        help='Number of initial infected people')
    parser.add_argument('--capacity', metavar='N', type=int, default=2000,
                        help='Hospitals healthcare capacity. 0 if unlimited capacity.')
    parser.add_argument('--lockdown', metavar='N', type=int, default=600,
                        help='Lockdown when cases reach a value. 0 if no lockdown at all.')
    parser.add_argument('--plot', action='store_true',
                        help='Generate plots instead of an animation')
    parser.add_argument('--file', metavar='N', type=str, default=None,
                        help='Filename to save to instead of showing on screen')
    args = parser.parse_args(args)

    # Set up the simulation
    simulation = Simulation(args.size, args.size,
                            args.recovery, args.infection, args.death,
                            args.capacity, args.lockdown, 
                            args.infectionCap, args.deathCap)
    simulation.population(args.population)
    simulation.infect_randomly(args.cases)
    
    # Obtain value args.population to be used in model_animation.py 
    get_ylim(args.population)

    # Plot or animation?
    if args.plot:
        fig = plot_simulation(simulation, args.duration)

        if args.file is None:
            #  python model_runsim.py --plot
            plt.show()
        else:
            #  python model_runsim.py --plot --file=plot.pdf
            fig.savefig(args.file)
    else:
        animation = Animation(simulation, args.duration)

        if args.file is None:
            #  python model_runsim.py
            animation.show()
        else:
            #  python model_runsim.py --file=animation.mp4
            #
            # NOTE: this needs ffmpeg to be installed.
            animation.save(args.file)
            

if __name__ == "__main__":
    #
    # CLI entry point. The main() function can also be imported and called
    # with string arguments.
    #
    import sys
    main(*sys.argv[1:])