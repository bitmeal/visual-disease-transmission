# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Copyright (C) 2020, Arne Wendt
#


class NoMask:
    riskTransmission = 1
    riskInfection = 1

class Surgical:
    riskTransmission = 0.5
    riskInfection = 0.5

class N95V:
    riskTransmission = 0.6
    riskInfection = 0.2
