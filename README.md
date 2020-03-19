# Visualizing Disease Transmission Prevention Mechanisms
The provided Scripts allow the simulation and visualization of disease transmission, for a configurable disease and with application of different methods to prevent spreading.

The disease is spread by human interaction. These interactions are purely statistical - no geometrical, behavioural or movement simulation is applied.

Following mechanisms for transmission prevention can be simulated and visualized:
* different types of protection equipment (masks)
* quarantine/isolation
* social-distancing/home-office with occasional outside contact

The building blocks of the Simulation are:
* **Disease:** The disease, adapting its properties (infectiousness, symptoms, immunity) over time
* **Person:** An entity that may contract and spread a disease by interaction. A person may perform actions depending on its infection, as *buying a mask* or *self-quarantining* on symptoms
* **Population:** A number of persons that may interact with each other
* **Protection:** Different types of devices limiting the risk of transmission
* **Protective measures:** quarantining or social-distancing

## Disease
A disease is spread by human interaction. Currently the risk for transmission without any protection equipment `= 1`. A disease is characterized by the following parameters:
* **latent period:** period after which the disease is infectious to others
* **incubation period:** period after infection to develop symptoms
* **duration:** total duration after infection

A person without a disease is *`HEALTHY`*. After contracting a disease, the person/disease passes the following phases, after the durations defined by `latentPeriod`, `incubationPeriod` and `duration` : *`INFECTED > SPREADING > SYMPTOMS`*

## Person
A person spreads a disease by human interaction. Each person is assumed a have a number of interactions per day, that qualify for disease transmission; characterized by the average number of interactions per day (`meanInteractionsPerDay`) and its standard deviation (`stddevInteractionsPerDay`), where currently:
```python
meanInteractionsPerDay = 2
stddevInteractionsPerDay = 1
```
If a person practices social-distancing / is in home-office, the behaviour is additionally characterized by the average number of consecutive days a person isolates itself (`meanConsecutiveDisable`). Say: A person interrupts its isolation every `n` days to *go shopping, etc.*. Currently assumed:
```python
meanConsecutiveDisable = 5
```
### Population
Persons in the same population interact with each other, thus spreading a disease. When persons practice social-distancing/home-office, they do not interact with any other person! (*A second, **passive** population is formed by all these persons.*) The randomly selected interactions between persons are sampled from the entirety of persons, thus implementing an important behaviour: When people stay at home, the population density decreases and reduces the chance for disease transmission. Sampling the interaction partners from the entirety of persons but respecting their state of social-distancing/home-office/isolation, effectively reduces the interactions per day, proportional to the number of people practicing social-distancing/home-office/isolation.

### Behaviour
A person can automatically react to its infection state. It is assumed, that a person only reacts when showing symptoms of the disease. Following two behaviours can be activated:
* Buying/Wearing a mask when showing symptoms
* Self-isolation when showing symptoms

## Protection
A person can protect itself and the community by using protective equipment. Using protective equipment, limits the risk for transmitting a disease and contracting a disease to different amounts. When no protective equipment is used, the risks for transmission and infection are *100%*:
```python
riskTransmission = 1.0
riskInfection = 1.0
```
Currently following types of protective equipment are defined:
> ***All values are assumptions and only used to illustrate the influence of different values for different parameters! These values do not reflect reality and shall only be used for relative comparison!***

#### Surgical Mask
A mask, reducing the risks for transmission and (self-)infection as follows:
```python
riskTransmission = 0.5
riskInfection = 0.5
```
#### N95 with valve
A mask, reducing the risks for transmission and (self-)infection as follows:
```python
riskTransmission = 0.6
riskInfection = 0.2
```
*Using a valve for exhaust air, directly pointed in direction of your **victim** and reducing the exhaust cross-section (compared to your mouth), thus increasing exhaust-air speed and travel distance, the risk for transmission is assumed to be higher compared to the surgical mask.*


# Simulation
### Script
The simulation can be configured by passing a python dictionary as string to the `dtps.py`-script. Following options are possible:
* `random_seed`: `int` Seed for the random number generator. A function such as `time.time()` can be passed, as the dictionary is 'evaluated'
* `population_size`: `int` Population size. ***Has to be the square of an integer number!***
* `init_infections`: `int` Initial number of infections in the population
* `init_mask_surgical`:  `int` Number of surgical masks to initially distribute to the population
* `init_mask_n95v`: `int` Number of N95 masks to initially distribute to the population
* `init_home_office`: `int` Persons to practice social-distancing/home-office from the beginning of the simulation
* `force_public_infections`: `bool` Force initial infections in public population; exclude persons in home-office/practicing social-distancing
* `second_population`: `bool` Draw the isolated population in a second plot
* `person_properties`: `dict` Dictionary configuring a persons behaviour, **see below**
* `sim_time`: `int` Duration of the simulation
* `filename`: `str` Animation filename, `.gif` automatically added as extension
* `fps`: `int` Animation frames per second

To configure the behaviour of a person, following options may be used:
* `mask_on_symptoms`: `bool` Buy/wear a mask when symptoms are showing
* `isolate_on_symptoms`: `bool` Isolate when symptoms are showing
* `default_mask`: `protection.Surgical or protection.N95V` Mask type to buy/wear, when `mask_on_symptoms = True`
* `interact_necessary_while_disabled`: `bool` Stay in social-isolation/home-office, or go shopping any few days?

Default configuration is: *400 persons, 2 infections, no masks or home-office and no automatic behavior for persons; 4 fps, 50 days and animation saved as `animation.gif`*

### Example
Following command line and parameters should produce the following output:
```bash
py viz.py "{'second_population': True, 'sim_time': 40, 'init_infections': 2, 'init_home_office': 100, 'person_properties':{'interact_necessary_while_disabled': True, 'mask_on_symptoms': True, 'default_mask': protection.N95V}, 'fps': 5, 'filename': 'viz-60d', 'random_seed': 5}"
```
### Visualization
Each square represents a person in the population. *The position is of no relevance and the geometrical layout does not influence the interaction of persons and the spread of the desease (they are purely statistical)*. Each square represents the same person throughout the simulation. Persons at the same position in both visualized populations represent the same person; each person can only be in either one at a time. The overlays show the protective equipment used by each person, the state of isolation/social-distancing/home-office (legend see below).
![example result visualization](./media/viz-60d.gif)

* &#8962; Persons in home-office/social-distancing
* &#10005; Persons in public; *not in second, passive population*
* &#10010; Persons in automatic, infection dependent isolation
* &#11096; N95 mask
* &#9723; Surgical mask