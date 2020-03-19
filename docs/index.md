---
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (C) 2020, Arne Wendt
#

layout: default
author: Arne Wendt
title: Visualizing Disease Transmission Prevention Mechanisms
image: /assets/img/static.png
---
{% include mathjax.html %}
{% assign figcounter = 0 %}

# Introduction
In light of the current events, it is necessary to understand how diseases are spreading and how different methods inhibit uncontrolled spreading. It is *especially important* to make this *information accessible and comprehensible* to an audience as broad as possible; this work is an attempt to make a contribution to that.


Following we will explore a simple simulation of how a disease spreads and different countermeasures that can be taken to limit the rate of spreading. After introducing our fictional disease, the population and their properties, step by step, different methods for controlling transmission and spreading of the disease are explored. After each method or a set of two similar measures, the simulations are discussed briefly in each **Findings**-subsection.


*The following simulation is purely statistical. Infections and human interactions are defined by probabilities and occur randomly. To develop an understanding of how spreading of a disease works on a "geometrical" level - by human movement and interaction - following article is recommended: [Why outbreaks like coronavirus spread exponentially, and how to "flatten the curve"](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/)*


<br/>
# Exploring the Simulation & Spreading without Countermeasures
{% include image.html url="assets/img/free-for-all.gif" description="Spreading the disease without protective and countermeasures. Population of 400 with 2 initial infections." %}

**Fig {{ lastfigure }}** shows how *two* initial infections spread in a population of *400* people, when no measures are taken. All following simulations assume an entirety of *400* persons and *two* initial infections. Let's explore...

### What Happened?
Each square in the visualization represents one person. Persons can contract and transmit the disease.
* Every person is assumed to have ***two* interactions** per day, that qualify for a **transmission of the disease**, at average
* The disease is assumed to have a **risk of transmission of *100%***
* From infection to recovery, the **disease lasts 15 days**

*Other parameters of the disease (incubation time, latent period, ...) are explored later. For further information about the simulation and its workings, visit the [github page](https://github.com/bitmeal/visual-disease-transmission).*

### Findings & How to Read the Visualization
From both the stackplot at the bottom and the population-grid, we can observe the following: There is a time where nearly all people are infected simultaneously. With a duration of 15 days for our infection, **infecting** the whole population **and full recovery takes 29 days**.

The *stackplot at the bottom* shows the distribution of infections and their state over time. It allows to visually assess the spreading and infection numbers over time. In the top right corner of the stackplot you find a counter `t = nn`, where `nn` is the current simulation time (number of days passed). The counter stops, once there are no infections in the population. The *population-grid at the top* shows the current state of infections at each time-step. The grid serves as a method to visually assess how the disease is spreading and how countermeasures are applied.

<br/>
# Protective equipment
Next we will try to understand the influence of protective equipment, worn be the individual, on the community. Two types of protective equipment with different characteristics are explored - both loosely modeled after common types of masks.

Protective equipment reduces the risk for disease transmission and contraction/infection. With $$p_t$$ being the probability of transmitting and $$p_c$$ being the probability of contracting a disease. The probability $$p_i$$ of an infection spreading from person *X* to person *Z* is: $$ p_i = p_{tX} * p_{cY} $$

In the following simulations, protective equipment is distributed to **a quarter of the population**.

### Mask S
{% include float.html url="assets/img/square.svg" %}
The first device to explore, we name *Mask S*. It protects its wearer and the community to equal parts, assuming following characteristics. The simulation and visualization is shown in **Fig {{ nextfigure }}**; *persons wearing* Mask S *are indicated by a white square with yellow border*.

$$
p_t = 0.5\\
p_c = 0.5
$$

{% include image.html url="assets/img/1of4-surgical.gif" description="Spreading the disease with $$1/4$$ of the population wearing *Mask S* with: $$p_t = 0.5 ; p_c = 0.5$$" %}


### Mask N
{% include float.html url="assets/img/circle.svg" %}
The second device to explore, we name *Mask N*. It protects its wearer and the community to *unequal* parts, assuming the characteristics below. The idea is to assess wether there is a difference in communal protection, when the probability for contracting a disease is significantly reduced, thus nearly eliminating these persons as an infection vector. The downside being an only slightly increased risk for transmission. Let's take a look at **Fig {{ nextfigure }}** and see what happens; *persons wearing* Mask N *are indicated by a white circle with yellow border*.

$$
p_t = 0.6\\
p_c = 0.2
$$

{% include image.html url="assets/img/1of4-n95.gif" description="Spreading the disease with $$1/4$$ of the population wearing *Mask N* with: $$p_t = 0.6 ; p_c = 0.2$$" %}

### Findings
Comparing the above simulations, issuing different protective equipment to the population, and the simulation without countermeasures, we obtain the following results:

Simulation | `t`: full recovery | `t`: majority recovery
---|---|---
*No measures* | $$29$$ | $$\approx27$$
*Mask S* | $$32$$ | $$\approx28$$
*Mask N* | $$39$$ | $$\approx29$$

What can be observed is, that the duration for full recovery of the population did increase about $$\approx33$$ in the case of *Mask N*. Looking at the stackplot in **Fig {{ lastfigure }}** we find, that the **majority** of persons **recovered after $$\approx29$$ days**. The biggest impact of using protective equipment is the gentle slope of the curve towards the populations full recovery.

> Use of protective equipment, with characteristics similar to the ones modeled above, by only $$1/4$$ of the population, seems to have a negligible effect on a diseases spreading.



<br/>
# Human behavior
{% include float.html url="assets/img/cross.svg" %}
In this step all persons will be equipped with some kind of *behavior* to react to the current state of their own infections. Two simulations will be run, with different responses to **symptoms of the infection showing**. To understand the behavior illustrated by the simulations we have to take a look at our disease and its properties first.

#### Properties of the disease
The simulated disease has the following properties and states; you can find these visualized according to the legend in all visualizations.

* **Infected** - a person carries the disease but is neither infectious nor shows any symptoms
* **Spreading** - after a *latent period* of **3 days**, the disease in infectious, but does not show symptoms
* **Symptoms** - the disease is spreading further and showing symptoms; *the first point in time for a person to notice its infection*
* **Immunity** - for the simulated disease, it is assumed that immunization occurs after an infection

### Using Protective Equipment on Symptoms
The visualization in **Fig {{ nextfigure }}** simulates spreading of the disease, while all people start using *Mask S* after showing symptoms.

{% include image.html url="assets/img/surgical-on-symptoms.gif" description="Spreading the disease while all persons start wearing a *Mask S* when showing symptoms." %}

### Isolating on Symptoms
**Fig {{ nextfigure }}** simulates spreading under the assumption that all persons isolate themselves immediately after showing symptoms. Persons isolating themselves are marked with &#10010;

{% include image.html url="assets/img/isolate-on-symptoms.gif" description="Spreading the disease, with all persons practicing isolation on onset of symptoms." %}


### Findings
We can observe that the duration, for a full infection and recovery of the population, does not differ significantly from the simulation without any measures to inhibit spreading.

Prior to taking countermeasures, of either using protective equipment or isolation, the disease has a period of 3 days to spread without any hindrance. Already this small time frame allows for a sufficiently high spread of the disease to not impact the overall spreading rate sufficiently.




<br/>
# Home-Office & Social-Distancing
{% include float.html url="assets/img/house.svg" %}
Another simple solution to inhibit disease spreading is *social-distancing* (e.g. working *home-office*, etc.). All scenarios, simulating the effect of countermeasures, explored til here, rely on either the distribution and availability of goods or are reactive - at a too-late point in the course of the disease. Where for the use of protective equipment, application by $$1/4$$ of the population was assumed, *social-distancing* is a *highly scalable* method to combat disease spreading. Due to this scalability, the following simulations visualize the effect of a **quarter** (**Fig {{ nextfigure }}**) of the population and additionally **half** (**Fig {{ nextfigure | plus: 1 }}**) the population practicing social-distancing.


While practicing social-isolation or working in home-office, people are assumed to still interact with the public to a limited amount. The simulation accounts for necessary interactions with the public (grocery shopping, etc.), by placing all persons from their isolation in the "public" for one day at average every 5 days. Persons practicing social-isolation further lower the population density in public. The number of interactions per person per day scales proportionally with the populations density - thus accounting for fewer interactions when fewer potential interaction partners are available. *(For further information about the simulation and its workings, visit the [github page](https://github.com/bitmeal/visual-disease-transmission))*


**Reading the Visualization:** The next visualizations feature two population-grids. The upper grid represents the "public". Persons in this population can infect and contract disease from each other. The bottom grid shows all people practicing social-distancing. *Persons in the bottom population do not interact and thus cannot infect each other!* People practicing social-distancing and are missing from the public, are marked with a &#8962;-symbol. In the bottom plot, people in public are marked with a &#10005;. A disease contracted in public is carried over to isolation and its evolution is visualized.

{% include image.html url="assets/img/1of4-home-office.gif" description="The effect of **quarter** of the population practicing *social-isolation*" %}

{% include image.html url="assets/img/1of2-home-office.gif" description="The effect of **half** the population practicing *social-isolation*" %}

### Findings
Social-distancing shows the highest effectiveness of all explored scenarios. Even with only a quarter of the population practicing, the number of persons being sick with symptoms at the same time is reduced, compared to all other scenarios. Increasing the share of persons practicing social-distancing has a noticeable effect on the infection rate and total number of simultaneous infections. All while being an easily and fast scalable measure.

<br/>
# Flattening the Curve
{% include float.html url="assets/img/curve.svg" %}
The following, last scenario (**Fig {{ nextfigure }}**) extends the previous one. Additionally to $$1/2$$ the population mostly staying at home, everybody showing symptoms quarantines themselves.

{% include image.html url="assets/img/1of2-home-office-isolation.gif" description="The effect of **half** the population practicing *social-isolation* and everybody isolating on the onset of symptoms of an infection." %}

#### Findings
The simulations shows effects that could not be observed in all other simulations before: After full recovery of the population and nobody to spread the disease again, $$\approx 1/3 to 1/3$$ have not been infected at all (see stackplot in **Fig {{ lastfigure }}**). The number of infected persons is seriously reduced and the time until full recovery of the population is prolonged, thus greatly reducing the number of persons infected simultaneously.


<br/>
# Conclusion

> **Stay safe and stay home. And if you have masks, give them to the elderly.**
> 
> *Staying at home is an effective and scalable measure; protective equipment is much less suitable in protecting the community.*

*Assuming half of the population staying at home and everybody isolating themselves on symptoms, the best case to *flatten the curve* could look as visualized in **Fig {{ figcounter | plus: 1 }}**. The infection is introduced to our sample of the population by two people practicing home-office/social-distancing and isolating themselves on the onset of symptoms - nobody gets hurt.*
{% include image.html url="assets/img/1of2-home-office-isolation-best-case.gif" description="A best case scenario" %}



<br/>
# Info
All information is provided to the best of our knowledge and belief. There is no claim to correctness and completeness.

<br/>
Get the code on github: [bitmeal/visual-disease-transmission](https://github.com/bitmeal/visual-disease-transmission)

All graphics above have been produced using the supplied script [`make_vizs.cmd`](https://github.com/bitmeal/visual-disease-transmission/blob/master/make_vizs.cmd) in the linked repository.

This sites content and the sources to create this content are licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/). &copy; Arne Wendt, 2020

