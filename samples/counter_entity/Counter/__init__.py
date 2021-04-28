import logging
import json

import azure.functions as func
import azure.durable_functions as df

# we can use global variables for caching; but they may reset between calls, at any time 
volatile_count = 0

def entity_function(context: df.DurableEntityContext):
    """A Counter Durable Entity.

    A simple example of a Durable Entity that implements
    a simple counter.

    Parameters
    ----------
    context (df.DurableEntityContext):
        The Durable Entity context, which exports an API
        for implementing durable entities.
    """

    # we use the global variable for the volatile count
    global volatile_count
 
    # we use the entity state for storing the persistent count
    persistent_count = context.get_state(lambda: 0)

    operation = context.operation_name

    
    if operation == "add": 
        # add the given argument to the count
        amount = context.get_input()
        volatile_count += amount
        persistent_count += amount

    elif operation == "reset":
        # reset the count
        current_value = 0
        a = 0

    elif operation == "get":
        # get the current count
        context.set_result((volatile_count,persistent_count))
        pass
    
    # write back the persistent count
    context.set_state(persistent_count)
    

main = df.Entity.create(entity_function)