# Python Epidemic Simulation

## Introduction
This project intends to simulate COVID-19 epidemic in Bristol and produce codes with high reusability so that it could be applied to predict and simulate future epidemics by tweaking the parameters. The model is then compared to the real world data to prove it's reliability.

## COVID-19 in Bristol 
The graph below shows the daily new cases of Covid 19 in the UK since March 2020 to May 2021.

![Plot of daily Covid-19 in the UK](https://user-images.githubusercontent.com/79267473/117594504-1d213d00-b136-11eb-8960-f2cc28776c37.png)

The graph below shows the daily deaths in the UK over the span of 14 months. 

![Plot of daily Covid-19 deaths in the UK](https://user-images.githubusercontent.com/79267473/117595928-fc5ae680-b139-11eb-9267-8237fbe71095.png)

# Simulation Runs
This project includes 2 simulation models:

**1. Simulation based on population in a grid (which can be found in [modified_model](https://github.com/Robbie-Mackay/Further-computing-project/tree/main/modified_model)):**

    $ python model_runsim.py 

**2. Simulation based on population acting as particles (which can be found in [main](https://github.com/Robbie-Mackay/Further-computing-project)):**

    $ python simulation.py

## Index
- [Simulation (Grid)](#simulation-grid)
    - [Simple Infection Simulation](#simple-infection-simulation)
    - [Simulating Healthcare Capacity and Lockdown](#simulating-healthcare-capacity-and-lockdown)
        - [Case: 'Limited Healthcare Capacity - Business As Usual'](#case-limited-healthcare-capacity---business-as-usual)
        - [Case: 'Unlimited Healthcare Capacity - Lockdown'](#case-unlimited-healthcare-capacity---lockdown)
        - [Case: 'Limited Healthcare Capacity - Lockdown'](#case-limited-healthcare-capacity---lockdown)
- [Simulation (Particles)](#simulation-particles)
- [Conclusion](#conclusion)

# Simulation (grid)
This simulation is based on the codes found in [this repository](https://github.com/oscar-uob/simulator.git).

Here is the summary of the changes and improvements that have been made by modifying the code:
- Add spaces between people (grey colour on grid)
- Ensure initial infected people are not repeated
- Add movement of people
- Additional features: lockdown and healthcare capacity
- Set default parameters that closely represent COVID-19 in reality  
- Improve code's versatality to simulate any epidemics
- Show number of people rather than percentage on the line graph
- Clearer animation with titles and legend


## Simple Infection Simulation
This is a simulation model of a polulation of people randomly moving around.
This is done by shuffling the 2D array storing the status of each person with the function below:
```ruby
np.random.shuffle() 
```
Parameters:
- Grid size: 10000
- Population: 6000 (hence 40% of the grid is the space/distance between people)
- Duration: 365 days
- Recovery probability: 0.02
- Infection probability: 0.03
- Death probability: 0.002

https://user-images.githubusercontent.com/79701244/118171697-68cc3300-b423-11eb-8d8e-6cff5f81bd1c.mp4

As shown in the simulation, the virus spreads quickly and almost everyone got infected, resulting in **538 fatalities** on the 365th day.

## Simulating Healthcare Capacity and Lockdown
To make the simulation as close to the reality as possible, limited healthcare capacity and lockdown measures are taken into consideration:
- When the cases are higher than the healthcare capacity, people infected could not be sent to the hospital to be isolated and treated. This increases the probabilities of infection and death.
- When cases are higher than a certain number, lockdown will be implemented. Therefore, people will stop moving around, reducing interaction.
The simulation results of the possible scenarios are shown below.

### Case 'Limited Healthcare Capacity - Business As Usual'
In this case, limited healthcare capacity is taken into account but the population is moving around as usual. The parameter set for the maximum healthcare capacity in this simulation is 2000.

https://user-images.githubusercontent.com/79701244/118171618-54883600-b423-11eb-9fa3-0333c7a2de1a.mp4

The simulation shows that the healthcare system becomes completely overwhelmed, leading to **929 fatalities** on the 365th day (15.5% of the population).

### Case 'Unlimited Healthcare Capacity - Lockdown'
In this case, lockdown is implemented when the number of cases is higher than the set parameter of 600. During lockdown, the population stops moving. Lockdown will be lifted when the number of cases drops below 600 and people are allowed to move around again as usual.

https://user-images.githubusercontent.com/79701244/118165262-028fe200-b41c-11eb-8008-8737023e28a6.mp4

Disregarding limited healthcare capacity, the simulation above shows that lockdown has only a little effect in reducing fatalities. Based on the simulation there is a total of **520 fatalities** on the 365th day (just 18 less than if there wasn't any lockdown.

### Case 'Limited Healthcare Capacity - Lockdown'
However, the significance of lockdown becomes apparent when both limited healthcare capacity is taken into account.

https://user-images.githubusercontent.com/79701244/118165346-176c7580-b41c-11eb-933e-587ac06bd003.mp4

Based on the simulation result, the **total fatality on the 365th day is 684** (26% lower than that of the case where lockdown is not being implemented).
Nevertheless, the simulation results are very close to the reality as shown [above](#COVID-19-in-Bristol), disregarding the first outbreak in April 2020.


# Simulation (particles)

This simulation models people as particles and includes an aspect of movement to simulate real world conditions. This model was inspired by a simulation seen at:   
https://scipython.com/blog/two-dimensional-collisions/  

Modifications have been made to model the infection, recovery and death.

Additional features: 
- Vaccination
- Duration of illness (This is done by importing the Time module to give each particle a reference to time)
- Different age groups 

The bar chart below shows real data based on the duration of illness of different age groups, taking genders into consideration.

![duration of illness UK](https://user-images.githubusercontent.com/79270716/118084417-9c25a800-b3b8-11eb-9b8f-586cfea16e05.png)

Summary of the functionalites of the program:
- Initally n number of particles are infected (red). Once the red infected particles collide with the blue susceptibles, it becomes infected and the changes to red colour.  
- User can enter an age group and based on real world data, the probability of death and the duration of infection will be appropriately selected and used in the  simulation.   
- The duration of illness will decide how long the particle will stay infected for. After this time period, the particle will turn from red to green (recovered).
- Based on the death probability, red particles will change their colour to black (dead).  

### Case 'Vaccination'

https://user-images.githubusercontent.com/79267473/118203103-43571d80-b453-11eb-971f-addcb1d03774.mp4

Based on the simulation, as vaccines are being rolled out, the infection rate decreases significantly.

### Case 'Vaccination - Older age group' 

People in the older age group are being vaccinated in a faster rate. 

https://user-images.githubusercontent.com/79267473/118203111-48b46800-b453-11eb-9c0a-0e3b8cfa3e1e.mp4

Based on the simulation above, though senior citizens have lower chances of recovery and higher chances of death, the effect of vaccination is crucial to keep the falalities to a minimum.

### Case - 'Vaccination - High number of initial cases'  
To gain a better perspective on the effect of vaccination in today's situation, that is, when the initial cases are already high, the following simulation features higher number of initial cases.

https://user-images.githubusercontent.com/79267473/118203119-4eaa4900-b453-11eb-9ac6-acbe004fdc53.mp4

The simulation above shows that despite greater number of initial cases, if people get vaccinated, the infection rate drops noticeably, therefore decreasing falalities. 

## Conclusion
Both simulation models work as intended. [Simulation (Grid)](#simulation-grid) proves it's reliability to simulate real life epidemic and [Simulation (Particles)](#simulation-particles) is able to represent movement of people in a clearer manner.

**Improvements and recommendations for future works**
- Combine the features of both simulations
- Modify the code so that some people are still able to move around during lockdown to represent frontline/essential workers
- Include "central locations" (such as city centre) to better represent Bristol
- Include a "self-isolation area" in the particle model
- Modify the codes to simulate pandemic rather than epidemic
