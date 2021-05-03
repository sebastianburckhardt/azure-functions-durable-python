import logging
import json

import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    """This orchestration function calls the entity. 

    We use one orchestration for each invocation because http triggered functions cannot receive a response directly from the entity.
    A side benefit is that each orchestration leaves a persistent record in storage.
    """
    request = context.get_input();
    entityId = df.EntityId("Counter", request['instance'])
    response = yield context.call_entity(entityId, "step", request)
    return response

main = df.Orchestrator.create(orchestrator_function)