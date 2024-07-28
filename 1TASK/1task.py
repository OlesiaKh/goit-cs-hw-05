import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile

parser = argparse.ArgumentParser(description="Sorting files")
parser.add_argument("--source", "-s", required=True, help="Source dir")
parser.add_argument("--output", "-o", help="Output dir", default="destination")
args = vars(parser.parse_args())

source = AsyncPath(args["source"])
output = AsyncPath(args["output"])


async def read_folder(path: AsyncPath):
    async for file in path.iterdir():
        if await file.is_dir():
            await read_folder(file)
        else:
            await copy_file(file)


async def copy_file(file: AsyncPath):
    folder = output / file.suffix[1:]
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(f"Error while copying {file}: {e}")


if __name__ == "__main__":
    if not source.exists():
        logging.error(f"Source directory '{source}' does not exist.")
        exit(1)
    else:
        format = "%(threadName)s %(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        asyncio.run(read_folder(source))

        print(f"All files copied to {output}. Source dir will be deleted")
