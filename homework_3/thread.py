import argparse
import shutil
from pathlib import Path
from threading import Thread, Semaphore
import logging

parser = argparse.ArgumentParser(description="App for sorting folder.")

parser.add_argument("-s", "--source", required=True, help="Path to sorting folder.")
parser.add_argument(
    "-d", "--destination", default="dist", help="Path to destination folder."
)
parser.add_argument(
    "-t", "--threads", default="2", help="Count of threads for sorting."
)
parser.add_argument(
    "-rb",
    "--removebase",
    default="0",
    help="{any int} to remove the base folder, 0 to leave.",
)

args = vars(parser.parse_args())
source = args.get("source")
destination = args.get("destination")
threads_count = int(args.get("threads"))
remove_base_folder = int(args.get("removebase"))

folders = []


def grab_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folder(el)


def sort_file(path: Path, semaphore: Semaphore):
    with semaphore:
        logging.debug(f"Got semaphore")
        for el in path.iterdir():
            if el.is_file():
                ext = el.suffix
                new_path = destination_folder / ext
                try:
                    new_path.mkdir(exist_ok=True, parents=True)
                    shutil.copyfile(el, new_path / el.name)
                except OSError as e:
                    logging.error(e)
        logging.debug(f"finished")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s, %(message)s")
    base_folder = Path(source)
    destination_folder = Path(destination)

    folders.append(base_folder)
    grab_folder(base_folder)

    threads = []
    semaphore = Semaphore(threads_count)
    for num, folder in enumerate(folders):
        thread = Thread(name=f"Th-{num}", target=sort_file, args=(folder, semaphore))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]

    if remove_base_folder:
        shutil.rmtree(base_folder)
        logging.debug("Base folder deleted.")
    else:
        logging.debug("Base folder not deleted.")
