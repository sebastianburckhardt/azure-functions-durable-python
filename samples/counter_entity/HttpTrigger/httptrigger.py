import logging

from azure.durable_functions import DurableOrchestrationClient
import azure.functions as func


async def main(
        req: func.HttpRequest,
        starter: str,
        ) -> func.HttpResponse:
    """Azure Function that handles incoming Http request from Jupyter and forwards it
    to the notebook entity, via an orchestration. 
    """

    try:  
        # collect all the data for this request
        request = {
            # the user identifies the counter instance to use
            'instance': req.params.get('instance'),
            # a sequence number for the step, starts with 0 for the initial state
            'step': req.params.get('step'),
        }

        # construct the DF client
        client = DurableOrchestrationClient(starter)

        # start an orchestration to perform this step
        instance_id = await client.start_new("invocation", None, request)
         
        # wait for a response, for a maximum of 200 seconds
        response = await client.wait_for_completion_or_create_check_status_response(req, instance_id, 200000);

        if type(response) is func.HttpResponse:
            # we timed out! Send status response, which contains URLs that can be used to check the status and re-request the final result
             return response
        else:
            # Send success response
             return func.HttpResponse(f"Result = {response}")

    except Exception as ex:
        # Send error response
        return func.HttpResponse(f"Exception = {ex}")
