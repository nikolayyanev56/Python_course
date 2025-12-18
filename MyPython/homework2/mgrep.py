import os
import sys
import argparse
from pathlib import Path
import shutil
from multiprocessing import Pool
import urllib.request
import tempfile
import re
#redo with regular expressions (thats "re")


class InvalidFileError(Exception):
    pass


class InvalidAmmountOfWorkers(Exception):
    pass


def search_in_file(pattern: re.Pattern, file_path: str, in_memory: bool) -> list[tuple[Path, int, str]]:
    """
    Searches for the given pattern line by line in the provided file path,\n
    unless in_memory is true, then it opens the whole file 
    """
    fp: Path = Path(file_path) 
    if not fp.exists() or not fp.is_file():
        raise InvalidFileError(f"Error {file_path} doesn't exist or isn't a file")
    
    res: list[tuple[str, int, str]] = []
    

    if in_memory:
        try:
            text = fp.read_text(encoding = "utf-8")  

        except Exception as ex:
            raise InvalidFileError(f"Error reading file {file_path}: {ex}")
        
        for l_num, line in enumerate(text.splitlines(), start = 1):
                if pattern.lower() in line.lower():
                    res.append((file_path, l_num, line))
                    
    else:
        try:
            with fp.open("r", encoding = "utf-8") as file:

                for l_num, line in enumerate(file, start = 1):
                    if pattern.lower() in line.lower():
                        res.append((file_path, l_num, line.rstrip("\n")))

        except Exception as ex:
            raise InvalidFileError(f"Error reading file {file}: {ex}")
        
    return res

            
def gather_work_file_paths(dir_paths: list[str]) -> list[Path]:

    """Finds all workable files under the given directories recursively"""

    work_files: list[Path] = []
    
    for fp in dir_paths:

        if os.path.isfile(fp):
            work_files.append(Path(fp))

        elif os.path.isdir(fp):
            for dirname, subdirs, files in os.walk(fp):
                for file in files:
                    work_files.append(Path(dirname) / file)

        else: continue
    
    return work_files

            
def worker_search_file(args: tuple[str, int, str]):

    """Used to map the search function onto the multithreading"""

    pattern, file_path, in_mem = args

    try:
        return search_in_file(pattern, file_path, in_mem)
    
    except InvalidFileError as f_err:
        pass


def run_multi_threaded(pattern: re.Pattern, files, in_memory: bool, line_num: bool, ammount_of_worker: int) -> None:
    """
    Runs the search processing in multiple threads given the ammount of workers
    """
    if ammount_of_worker < 0:
        raise InvalidAmmountOfWorkers("Not enough workers!")
    
    if ammount_of_worker > len(files):
        raise InvalidAmmountOfWorkers("More workers than files!")
    
    res: list[tuple[str, int, str]] = []

    if ammount_of_worker == 0 or len(files) == 0:
        for file in files:

            temp = search_in_file(pattern, file, in_memory)
            for item in temp:
                res.append(item)

    else:
        with Pool(processes = ammount_of_worker) as pool:
            
            work = [(pattern, f, in_memory) for f in files]
            completed_work = pool.map(worker_search_file, work)

            for complete in completed_work:
                for tup in complete:
                    res.append(tup)
    
    for item in res:
        f_p, line_number, txt = item
        str_path = str(f_p)
        if line_num:
            print(f"{str_path}:{line_number} - {txt}")
        else:
            print(f"{str_path} - {txt}")
    

def download_urls(urls: list[str], temp_dir: Path) -> list[Path]:
    """
    Downloads all urls in a temporary file to search in\n
    and returns a list of the locations of the temporary files
    """
    local_files: list[Path] = []
    
    for url in urls:

        try:
            resp = urllib.request.urlopen(url)
            data = resp.read()

        except Exception as e:
            print(f"Error when reading file at URL {url}: {e}", file=sys.stderr)
            continue

        local_name = url.rstrip('/').split('/')[-1] or "downloaded_file"
        local_path = temp_dir / local_name
        
        try:
            with open(local_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            print(f"Error when writing downloaded file {local_path}: {e}", file=sys.stderr)
            continue

        local_files.append(local_path)

    return local_files


def main():

    parser = argparse.ArgumentParser(prog = "mgrep.py")
    
    parser.add_argument("-n", "--line-number", action = "store_true")
    parser.add_argument("-m", "--in-memory", action = "store_true", help = "Show this help message and exit")
    parser.add_argument("-p", "--parallel", help = "Number of parallel searches", default = 0, type = int)

    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument("-r", "--recursive", action = "store_true", help = "Recursive search of all the files in the directory")
    exclusive.add_argument("-u", "--from_url", action = "store_true", help = "Search in files of url adresses")

    parser.add_argument("pattern", help = "Template to search", type = str)
    parser.add_argument("files", nargs = "*", help = "Files to search in", type = str)

    args = parser.parse_args()
    line_num = args.line_number
    mem = args.in_memory
    workers = args.parallel
    url = args.from_url
    rec = args.recursive
    try:
        search_pattern = re.compile(args.pattern)
    except re.error as err:
        print(f"Invalid regular expression: {e}", file=sys.stderr)
        sys.exit(1)

    file_paths = args.files
    
    work_file_paths = []

    url_temp = None

    if url:
        #temporarily download the content
        tmp = tempfile.mkdtemp(prefix = "mgrep_temp")
        url_temp = Path(tmp)
        local = download_urls(file_paths, url_temp)
        work_file_paths = local

    elif rec:
        work_file_paths = gather_work_file_paths(file_paths)

    else:

        for f in file_paths:
            if os.path.isfile(f):
                work_file_paths.append(f)         
         

    try:
        run_multi_threaded(search_pattern, work_file_paths, mem, line_num, workers)

    except InvalidAmmountOfWorkers as w:
        print(f"Invalid ammount of workers: {w}")

    finally:
        if url_temp is not None:
            try:
                shutil.rmtree(url_temp)
            except Exception as e:
                print(f"Error occured: {e}")


if __name__ == "__main__":
    main()
