from multiprocessing import Process, Queue
import folder_listener
import job_processor
import logging
import logging.config
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(processName)s-%(levelname)s-%(message)s")
logger.addHandler(handler)


def run():
    job_queue = Queue()
    logging.info("Starting processes")
    job_process = Process(
        target=job_processor.run,
        args=(job_queue,),
        name="job_processor",
        daemon=True,
    )
    job_process.start()
    listener_process = Process(
        target=folder_listener.run,
        args=(job_queue,),
        name="folder_listener",
        daemon=True,
    )
    listener_process.start()

    job_process.join()
    listener_process.join()


if __name__ == "__main__":
    run()

