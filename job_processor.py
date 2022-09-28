import logging
import asyncio
import queue
import os
import importlib
import shutil
import json

OUTPUT_PATH = f"{os.environ.get('TRAINML_OUTPUT_PATH')}/processed"


async def init():
    os.makedirs(f"{OUTPUT_PATH}", exist_ok=True)
    predict = importlib.import_module("simple-tensorflow-classifier.predict")
    return predict


async def job_processor(job_queue):
    predict = await init()
    while True:
        try:
            (file_name, file_path) = job_queue.get(False)
            result = predict.predict_image(file_path)
            shutil.copy(file_path, f"{OUTPUT_PATH}/{file_name}")
            with open(f"{OUTPUT_PATH}/{file_name}-results.json", "w") as f:
                f.write(json.dumps(result))
            logging.info(f"{file_name} - {result}")
            os.remove(file_path)
        except queue.Empty:
            pass
        await asyncio.sleep(0.01)


def run(job_queue):
    logging.info("Starting job processor")

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(job_processor(job_queue))
    finally:
        event_loop.close()

