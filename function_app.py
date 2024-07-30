import azure.functions as func
import logging
import azure.durable_functions as df
from openai import AzureOpenAI
import os

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

OPENAI_EMBEDDINGS_ENDPOINT = os.getenv("Openai.Endpoint")
OPENAI_EMBEDDINGS_KEY = os.getenv("Openai.ApiKey")
OPENAI_EMBEDDINGS_VERSION = os.getenv("Openai.ApiVersion")


# client = AzureOpenAI(
#     api_key=OPENAI_EMBEDDINGS_KEY,
#     azure_endpoint = OPENAI_EMBEDDINGS_ENDPOINT,
#     api_version = OPENAI_EMBEDDINGS_VERSION
# )

# An HTTP-Triggered Function with a Durable Functions Client binding
@myApp.route(route="orchestrators/answersgenerator", methods=["POST"])
@myApp.durable_client_input(client_name="client")
async def http_trigger(req: func.HttpRequest, client) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        req_body = req.get_json()
        instance_id = await client.start_new("answer_generator_orchestrator", None, req_body)
        response = client.create_check_status_response(req, instance_id)
        
        return response
        # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    

@myApp.orchestration_trigger(context_name="context")
def answer_generator_orchestrator(context):
    client = AzureOpenAI(
        api_key=OPENAI_EMBEDDINGS_KEY,
        azure_endpoint = OPENAI_EMBEDDINGS_ENDPOINT,
        api_version = OPENAI_EMBEDDINGS_VERSION
    )
    return "Hola"