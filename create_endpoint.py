import asyncio
import argparse

from trainml.trainml import TrainML

parser = argparse.ArgumentParser(
    description="Regional File Listener Classification Endpoint"
)

parser.add_argument(
    "datastore_id",
    type=str,
    help="Regional datastore ID containing the folder to listen for new files on",
)

parser.add_argument(
    "datastore_path",
    type=str,
    help="Path within the regional datastore to listen to new files on",
)


async def create_endpoint(trainml, datastore_id, datastore_path):
    job = await trainml.jobs.create(
        "Test Endpoint File Listener",
        type="endpoint",
        gpu_type="GTX 1060",
        gpu_count=1,
        disk_size=10,
        endpoint=dict(start_command="python main.py"),
        model=dict(
            source_type="git",
            source_uri="https://github.com/trainML/file-listener-endpoint.git",
        ),
        data=dict(
            output_type="regional",
            output_uri=datastore_id,
            output_options=dict(path=datastore_path),
        ),
    )
    return job


if __name__ == "__main__":
    args = parser.parse_args()
    trainml = TrainML()
    job = asyncio.run(
        create_endpoint(trainml, args.datastore_id, args.datastore_path)
    )
    asyncio.run(job.wait_for("running"))
    print("Job ID: ", job.id, " Running")

