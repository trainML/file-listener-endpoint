import logging
import asyncio
import tempfile
import os
import shutil

INCOMING_PATH = f"{os.environ.get('TRAINML_OUTPUT_PATH')}/incoming"


async def init():
    logging.info(f"{os.listdir(os.environ.get('TRAINML_OUTPUT_PATH'))}")
    os.makedirs(f"{INCOMING_PATH}", exist_ok=True)


async def folder_listener(job_queue):
    await init()
    while True:
        contents = os.listdir(INCOMING_PATH)
        for file in contents:
            filename = file
            _, file_path = tempfile.mkstemp()
            shutil.copy(f"{INCOMING_PATH}/{filename}", file_path)
            os.remove(f"{INCOMING_PATH}/{filename}")
            logging.info(f"Copied {filename} to {file_path}")
            job_queue.put((filename, file_path))

        await asyncio.sleep(1)


def run(job_queue):
    logging.info("Starting folder listener")

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(folder_listener(job_queue))
    finally:
        event_loop.close()

