import logging
import json

import azure.functions as func
import azure.durable_functions as df

# we cache counter instances in a dictionary
cached_states = {}

def initial_state():
    return { 'version': 0, 'count' : 0 }

def entity_function(context: df.DurableEntityContext):

    request = context.get_input();

    # first, try to get the state from the cache
    global cached_states
    state = cached_states.pop(context.entity_key, None)

    # if not found, or not the right version, read from the entity state
    if (state == None or state['version'] != int(request['step'])):
        state = context.get_state(initial_state)
    
    # check for consistency, and increment version number
    if state['version'] != int(request['step']):
        raise Exception(f"step number {int(request['step'])} does not match state version {state['version']}")
    state['version'] = state['version'] + 1

    # execute the operation
    state['count'] = state['count'] + 1

    # update the entity state and the cache
    context.set_state(state)
    cached_states[context.entity_key] = state
    
    # return the response
    response = {
        'version' : state['version'],
        'count' : state['count']
    }
    context.set_result(response)    

main = df.Entity.create(entity_function)