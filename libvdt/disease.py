# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (C) 2020, Arne Wendt
#


from enum import Enum, auto, IntEnum


class Disease:

    class infectionState(IntEnum):
        IMMUNE = 0
        HEALTHY = 1
        INFECTED = 5
        SPREADING = 7
        SYMPTOMS = 9


    incubationPeriod = 5
    latentPeriod = 3
    duration = incubationPeriod + 10

    def __init__(self):
        self.age = 0
    
    def tick(self):
        self.age += 1

    def isInfected(self):
        if self.age <= self.duration:
            return True
        else:
            return False

    def hasSymptoms(self):
        if not self.isInfected(): return False
        if self.age >= self.incubationPeriod:
            return True
        else:
            return False

    def isInfectious(self):
        if not self.isInfected(): return False
        if self.age >= self.latentPeriod:
            return True
        else:
            return False

    # disease starts as infected, if disease is instatiated and infected is false, we had it and are immune now
    def isImmune(self):
        return not self.isInfected()

    def state(self):
        if self.isImmune() : return self.infectionState.IMMUNE
        if self.hasSymptoms() : return self.infectionState.SYMPTOMS
        if self.isInfectious() : return self.infectionState.SPREADING
        if self.isInfected() : return self.infectionState.INFECTED