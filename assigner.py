#!/usr/bin/env python
# coding: utf-8

import yaml
from responses import *

def assign_response(message):

    message = message.lower()

    words = message.split(' ')

    if words[0] == '.pasquale':

        return build_pasquale_response(words[1])

    if message == '.cilia':
        return build_cilia_response()

    elif message == '.boulas':
        return build_boulas_response()
 
    elif message == '.idelber':
        return build_idelber_response()

    elif message == '.fazzi':
        return build_fazzi_response()

    elif message in ['.brasil-autoctone','.braut']:
        return build_braut_response()

    elif message == '.lucyborn':
        return build_lucyborn_response()

    elif message == '.pupo':
        return build_pupo_response()

    elif message == '.assis':
        return build_assis_response()
    
    elif message == '#paradox':
        return build_nazi_response()

    elif message == '.gamers':
        return build_gamers_response()

    elif words[0] in ['.salario','.salário']:
        return build_salario_response(words[1])

    else:
        return build_random_response()
