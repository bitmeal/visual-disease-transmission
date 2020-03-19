# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (C) 2020, Arne Wendt
#


import random

from libvdt.disease import *
from libvdt import protection

# states to visualize:
#   - healthy   = 1
#   - infected  = 5
#   - spreading = 7
#   - symptoms  = 9
#   - immune    = 0


class Person:

    meanInteractionsPerDay = 2
    stddevInteractionsPerDay = 1

    meanConsecutiveDisable = 5

    def __init__(self, population, **kwargs): #population: List[Person]
        self.enabled = True
        self.enabledToday = self.enabled
        self.isolated = False
        self.protection = protection.NoMask
        self.disease = None
        self.population = population
        self.age = 0
        self.infectedOn = None
        self.interactions = 0
        self.interactionsToday = max(int(random.gauss(self.meanInteractionsPerDay, self.stddevInteractionsPerDay) - self.interactions), 0)
        self.ID = len(population)
        self.maskOnSymptoms = kwargs.get('mask_on_symptoms', False)
        self.isolateOnSymptoms = kwargs.get('isolate_on_symptoms', False)
        self.defaultMask = kwargs.get('default_mask', protection.Surgical)
        self.interactNecessaryWhileDisabled = kwargs.get('interact_necessary_while_disabled', False)
    
    def infectStatic(self):
        self.disease = Disease()
        self.infectedOn = self.age #copy

    def infect(self, source):
        if not self.enabledToday : return
        if self.disease != None: return
        if random.random() < (self.protection.riskInfection * source.protection.riskTransmission):
            self.infectStatic()

    def spread(self, target):
        if not self.enabledToday : return
        if (
            self.disease == None or # healthy
            self.age <= self.infectedOn or # "spreading" not finished for this round
            not self.disease.isInfectious()
        ):
            return
        
        target.infect(self)


    def interact(self):
        antisocialTargets = [p for p in self.population if (p.interactions < p.meanInteractionsPerDay and p != self)]
        #random.shuffle(targets)
        maxSamples = min(self.interactionsToday, len(antisocialTargets))
        targets = random.sample(antisocialTargets, maxSamples)
        for target in targets:
            self.spread(target)
            target.spread(self)
            target.interactions += 1
            self.interactions += 1

    def behave(self):
        if (
            self.interactNecessaryWhileDisabled and
            random.random() < 1/self.meanConsecutiveDisable and
            not self.isolated
        ): self.enabledToday = True

        if self.disease != None:
            if self.maskOnSymptoms and self.disease.hasSymptoms() and self.protection == protection.NoMask :
                self.protection = self.defaultMask

            if self.isolateOnSymptoms and self.disease.hasSymptoms() :
                self.enabled = False
                self.enabledToday = False
                self.isolated = True

            if self.disease.isImmune():
                self.protection = protection.NoMask
                self.enabled = True
                self.enabledToday = True
                self.isolated = False


    def prepare(self):
        self.enabledToday = self.enabled
        self.interactions = 0
        self.interactionsToday = max(int(random.gauss(self.meanInteractionsPerDay, self.stddevInteractionsPerDay) - self.interactions), 0)

    def tick(self):
        if self.disease != None:
            self.disease.tick()
        self.behave()
        self.interact()
        self.age += 1

    def getEnable(self, **kwargs):
        return ((kwargs.get('invert_enable', False) != self.enabledToday) or kwargs.get('override_enable', False))

    def state(self):
        if self.disease == None :
            return Disease.infectionState.HEALTHY
        else :
            return self.disease.state()

    def displayState(self, **kwargs):
        if not self.getEnable(**kwargs) :
            return Disease.infectionState.HEALTHY
        else :
            return self.state()
