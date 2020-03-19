#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (C) 2020, Arne Wendt
#

import sys
import random
import time
import math
import numpy
import seaborn
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from celluloid import Camera
from libvdt.person import *
from libvdt.disease import *
from libvdt import protection

# parse parameters
if len(sys.argv) > 1:
    try:
        kwargs = eval(sys.argv[1])
        if not isinstance(kwargs, dict): raise
        print("Configuring from dictionary: ", kwargs)
    except:
        print ("Could not interpret argument as dictionary! Exiting")
        quit(1)




# setup
# defaults
randomSeed = time.time()
populationSize = 20 **2
initialInfections = 2
initialSurgicalMasks = 0
initialN95VMasks = 0
initialHomeOffice = 0
printSecondPopulation = False
forceInfectionsInPublic = False

personProps = dict()

simTime = 50

filename = 'animation'
fps = 4

# get arguments
randomSeed = kwargs.get('random_seed', randomSeed)
populationSize = int(kwargs.get('population_size', populationSize))
initialInfections = int(kwargs.get('init_infections', initialInfections))
initialSurgicalMasks = int(kwargs.get('init_mask_surgical', initialSurgicalMasks))
initialN95VMasks = int(kwargs.get('init_mask_n95v', initialN95VMasks))
initialHomeOffice = int(kwargs.get('init_home_office', initialHomeOffice))
printSecondPopulation = kwargs.get('second_population', printSecondPopulation)
personProps = kwargs.get('person_properties', personProps)
simTime = int(kwargs.get('sim_time', simTime))
filename = kwargs.get('filename', filename)
fps = int(kwargs.get('fps', fps))
forceInfectionsInPublic = kwargs.get('force_public_infections', forceInfectionsInPublic)

# impl
random.seed(randomSeed)

def getMarkers(population, condition):
    markerX = [(p.ID % int(math.sqrt(populationSize)) + 0.5) for p in population if condition(p)]
    markerY = [int(p.ID / math.sqrt(populationSize)) + 0.5  for p in population if condition(p)]
    return markerX, markerY


# build population
population = []
for i in range(populationSize):
    population.append(Person(population, **personProps))

# distribute masks
for person in random.sample([p for p in population if p.protection == protection.NoMask], initialSurgicalMasks):
    person.protection = protection.Surgical
for person in random.sample([p for p in population if p.protection == protection.NoMask], initialN95VMasks):
    person.protection = protection.N95V

# homeoffice
for person in random.sample([p for p in population if p.protection == protection.NoMask], initialHomeOffice):
    person.enabled = False

# init population infection
for target in random.sample([p for p in population if (p.getEnable() if forceInfectionsInPublic else True)], initialInfections):
    target.infectStatic()



# plot
if printSecondPopulation:
    fig, ax = plt.subplots(3, figsize=(10,22), gridspec_kw=dict(height_ratios=[8,1,8]))
else:
    fig, ax = plt.subplots(2, figsize=(10,12), gridspec_kw=dict(height_ratios=[8,1]))
    
ax[1].set_xlim([0, simTime - 1])
camera = Camera(fig)

cmap='GnBu'
cmapInst = plt.cm.get_cmap('GnBu')
cmapDiscrete = [
    cmapInst(int(Disease.infectionState.SYMPTOMS)/10),
    cmapInst(int(Disease.infectionState.SPREADING)/10),
    cmapInst(int(Disease.infectionState.INFECTED)/10),
    cmapInst(int(Disease.infectionState.HEALTHY)/10),
    cmapInst(int(Disease.infectionState.IMMUNE)/10)
]

legend =[
    Line2D([0], [0], label='Immune', color='none', markeredgecolor='none', markerfacecolor=cmapDiscrete[4], marker='s', markersize=20),
    Line2D([0], [0], label='Healthy', color='none', markeredgecolor='none', markerfacecolor=cmapDiscrete[3], marker='s', markersize=20),
    Line2D([0], [0], label='Infected', color='none', markeredgecolor='none', markerfacecolor=cmapDiscrete[2], marker='s', markersize=20),
    Line2D([0], [0], label='Spreading', color='none', markeredgecolor='none', markerfacecolor=cmapDiscrete[1], marker='s', markersize=20),
    Line2D([0], [0], label='Symptoms', color='none', markeredgecolor='none', markerfacecolor=cmapDiscrete[0], marker='s', markersize=20)
]
# history/stackplot
history = [[], [], [], [], []]


for timeStep in range(simTime):
    for p in population:
        p.prepare()

    for p in population:
        p.tick()

    infectionMap = [int(p.displayState()) for p in population]
    infectionMap = numpy.asarray(infectionMap).reshape((int(math.sqrt(populationSize)), int(math.sqrt(populationSize))))
    seaborn.heatmap(infectionMap,
        linewidths=0.5, linecolor='white',
        yticklabels=False, xticklabels=False, cbar=False, square=True,
        rasterized=False,
        vmin=0, vmax=10, cmap=cmap,
        ax=ax[0])
    
    markerXPPE, markerYPPE = getMarkers(population, lambda p: p.protection == protection.N95V and p.getEnable())
    ax[0].scatter(markerXPPE, markerYPPE, s=150, marker='o', edgecolors='y', facecolors='w')

    markerXCPE, markerYCPE = getMarkers(population, lambda p: p.protection == protection.Surgical and p.getEnable())
    ax[0].scatter(markerXCPE, markerYCPE, s=150, marker='s', edgecolors='y', facecolors='w')

    markerXDis, markerYDis = getMarkers(population, lambda p: not p.getEnable() and not p.isolated)
    ax[0].scatter(markerXDis, markerYDis, s=300, marker='$\u2302$', edgecolors='#cdcdcd', facecolors='none')

    if not printSecondPopulation:
        markerXQuar, markerYQuar = getMarkers(population, lambda p: p.isolated)
        ax[0].scatter(markerXQuar, markerYQuar, s=275, marker='P', edgecolors='#cdcdcd', facecolors='y')#'#fd9100')


    ax[0].legend(handles=legend, loc='lower left', ncol=5, bbox_to_anchor=(-0.015, -0.085, 1.015, 1), mode='expand', prop={'size': 15}, handletextpad=0.075, frameon=False, borderaxespad=0 )

    history[0].append(len([p for p in population if p.state() == Disease.infectionState.SYMPTOMS]))
    history[1].append(len([p for p in population if p.state() == Disease.infectionState.SPREADING]))
    history[2].append(len([p for p in population if p.state() == Disease.infectionState.INFECTED]))
    history[3].append(len([p for p in population if p.state() == Disease.infectionState.HEALTHY]))
    history[4].append(len([p for p in population if p.state() == Disease.infectionState.IMMUNE]))
    ax[1].stackplot(range(timeStep +1 ), history, colors=cmapDiscrete)
    ax[1].axis('off')

    text_kwargs = dict()
    if(
        history[0][-1] != 0 or
        history[1][-1] != 0 or
        history[2][-1] != 0 
    ) :
        displayStep = timeStep
    else :
        text_kwargs.update(color = cmapDiscrete[0])


    ax[1].text(0.88*(simTime-1), 0.7*populationSize, "t =", size=15, ha='left')
    ax[1].text(0.98*(simTime-1), 0.7*populationSize, str(displayStep), size=15, ha='right', **text_kwargs)


    if printSecondPopulation:
        infectionMap = [int(p.displayState(invert_enable=True)) for p in population]
        infectionMap = numpy.asarray(infectionMap).reshape((int(math.sqrt(populationSize)), int(math.sqrt(populationSize))))
        seaborn.heatmap(infectionMap,
            linewidths=0.5, linecolor='white',
            yticklabels=False, xticklabels=False, cbar=False, square=True,
            rasterized=False,
            vmin=0, vmax=10, cmap=cmap,
            ax=ax[2])
        
        markerXPPE, markerYPPE = getMarkers(population, lambda p: p.protection == protection.N95V and not p.getEnable())
        ax[2].scatter(markerXPPE, markerYPPE, s=150, marker='o', edgecolors='y', facecolors='w')

        markerXCPE, markerYCPE = getMarkers(population, lambda p: p.protection == protection.Surgical and not p.getEnable())
        ax[2].scatter(markerXCPE, markerYCPE, s=150, marker='s', edgecolors='y', facecolors='w')

        #markerXDis, markerYDis = getMarkers(population, lambda p: not p.getEnable() and not p.isolated and p.protection == protection.NoMask)
        #ax[2].scatter(markerXDis, markerYDis, s=300, marker='$\u2302$', edgecolors='y', facecolors='none')

        markerXDis, markerYDis = getMarkers(population, lambda p: p.getEnable())
        ax[2].scatter(markerXDis, markerYDis, s=300, marker='x', edgecolors='#cdcdcd', facecolors='#cdcdcd')

        markerXQuar, markerYQuar = getMarkers(population, lambda p: p.isolated)
        ax[2].scatter(markerXQuar, markerYQuar, s=275, marker='P', edgecolors='#cdcdcd', facecolors='y')#'#fd9100')

        




    camera.snap()

anim = camera.animate(blit=False)
anim.save(filename + '.gif', writer='imagemagick', fps=fps)
