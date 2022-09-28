<div align="center">
  <a href="https://www.trainml.ai/"><img src="https://www.trainml.ai/static/img/trainML-logo-purple.png"></a><br>
</div>

# Regional File Listener Endpoint Example

### Prerequisites

Before beginning this example, ensure that you have satisfied the following prerequisites.

- A valid [trainML account](https://auth.trainml.ai/login?response_type=code&client_id=536hafr05s8qj3ihgf707on4aq&redirect_uri=https://app.trainml.ai/auth/callback) with a non-zero [credit balance](https://docs.trainml.ai/reference/billing-credits/)
- A python virtual environment with the [trainML CLI/SDK](https://github.com/trainML/trainml-cli) installed and [configured](https://docs.trainml.ai/reference/cli-sdk#authentication).
- At least one GPU system onboarded with [CloudBender™](https://docs.trainml.ai/reference/cloudbender/)
- A writeable Regional Datastore configured in the same region as the CloudBender GPU system.

## Create the trainML Endpoint

To create the endpoint, run the following command from a python virtual environment with the [trainML CLI/SDK](https://github.com/trainML/trainml-cli) installed and [configured](https://docs.trainml.ai/reference/cli-sdk#authentication)

```
python create_endpoint.py DATASTORE_ID DATASTORE_PATH
```

where `DATASTORE_ID` is the ID of the regional datastore that will host the files to perform inference on, and `DATASTORE_PATH` is the subdirectory within that regional datastore to build the "incoming" and "processed" folders that the endpoint uses.

## Activate the endpoint

Add new image files to the same regional datastore you configure above inside the "incoming" folder of the specified datastore path.  In a few seconds, the file will be removed from the incoming folder, and rewritten to the "processed" folder, with an additional file with the suffix `-results.json` that contains the model predictions.