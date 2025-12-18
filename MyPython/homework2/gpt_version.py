#!/usr/bin/env python3
import argparse
import re
import os
import sys
import tempfile
import shutil
from pathlib import Path
from multiprocessing import Pool
from typing import List, Tuple, Optional, Union
import urllib.request

class InvalidFileError(Exception):
    pass

class InvalidAmountOfWorkers(Exception):
    pass

def search_in_file(pattern: re.Pattern, file_path: Union[str, Path], is_in_memory: bool) -> List[Tuple[str, int, str]]:
    """
    Търси pattern във file_path. Ако is_in_memory, зарежда целия файл, иначе — чете строчка по строчка.
    Връща списък от tuple: (filename, line_number, line_content).
    Ако файлът не съществува -> хвърля InvalidFileError.
    """
    fp = Path(file_path)
    if not fp.exists() or not fp.is_file():
        raise InvalidFileError(f"File {file_path} does not exist or is not a file")

    results: List[Tuple[str, int, str]] = []
    filename = str(fp)

    if is_in_memory:
        try:
            text = fp.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            raise InvalidFileError(f"Error reading file {file_path}: {e}")
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                results.append((filename, i, line))
    else:
        try:
            with fp.open('r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, start=1):
                    if pattern.search(line):
                        results.append((filename, i, line.rstrip('\n')))
        except Exception as e:
            raise InvalidFileError(f"Error reading file {file_path}: {e}")

    return results

def _worker_search(args):
    # помощна функция за multiprocessing Pool
    pattern, file_path, is_in_memory = args
    try:
        return search_in_file(pattern, file_path, is_in_memory)
    except InvalidFileError as e:
        # Можеш да избереш: да записваш грешки или да ги игнорираш
        return []

def run_multi_threaded(pattern: re.Pattern, files: List[Union[str, Path]], is_in_memory: bool,
                       is_line_numbers: bool, amount_of_workers: int) -> None:
    """
    Паралелно търсене в files с amount_of_workers процеса.
    Ако amount_of_workers == 0 => търси в текущия процес.
    Печата резултатите (file:line_number: line) или (file: line).
    """
    if amount_of_workers < 0:
        raise InvalidAmountOfWorkers("Number of workers must be >= 0")

    n_files = len(files)
    if amount_of_workers > n_files:
        raise InvalidAmountOfWorkers("More workers than files")

    results: List[Tuple[str, int, str]] = []
    if amount_of_workers == 0 or n_files == 0:
        # Синхронно
        for f in files:
            results.extend(search_in_file(pattern, f, is_in_memory))
    else:
        # Паралелно посредством Pool
        with Pool(processes=amount_of_workers) as pool:
            tasks = [(pattern, f, is_in_memory) for f in files]
            all_res = pool.map(_worker_search, tasks)
            for sub in all_res:
                results.extend(sub)

    for filename, lineno, line in results:
        if is_line_numbers:
            print(f"{filename}:{lineno} - {line}")
        else:
            print(f"{filename} - {line}")

def gather_files_from_dirs(paths: List[Union[str, Path]]) -> List[Path]:
    """
    За recursive режим: обход на директории и събиране на всички файлове.
    """
    files: List[Path] = []
    for p in paths:
        p0 = Path(p)
        if p0.is_dir():
            for dirpath, _, filenames in os.walk(p0):
                for fn in filenames:
                    files.append(Path(dirpath) / fn)
        elif p0.is_file():
            files.append(p0)
        else:
            # пропускаме невалидни пътища
            continue
    return files

def download_urls(urls: List[str], temp_dir: Path) -> List[Path]:
    """
    Сваля всеки URL в temp_dir, връща списък с локалните пътища на свалените файлове.
    Ако не успее за даден URL — принтира грешка и пропуска.
    """
    local_files: List[Path] = []
    for url in urls:
        try:
            resp = urllib.request.urlopen(url)
            data = resp.read()
        except Exception as e:
            print(f"Error when reading file at URL {url}: {e}", file=sys.stderr)
            continue
        # формируем име на файл
        # може да вземем името от URL или да дадем уникално
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
    parser = argparse.ArgumentParser(description='mgrep — паралелна grep-подобна команда')
    parser.add_argument('-n', '--line-number', action='store_true', help='Показване на номера на редовете')
    parser.add_argument('-m', '--in-memory', action='store_true', help='Зареждане на целия файл в паметта преди търсене')
    parser.add_argument('-p', '--parallel', type=int, default=0,
                        help='Брой паралелни търсения (0 = без паралелност)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--recursive', action='store_true', help='Рекурсивно търсене в директории')
    group.add_argument('-u', '--from-url', action='store_true', help='Търсене във файлове от URL адреси')
    parser.add_argument('pattern', help='Шаблон (регулярен израз) за търсене')
    parser.add_argument('files', nargs='*', help='Файлове или директории или URL-та')

    args = parser.parse_args()

    try:
        compiled = re.compile(args.pattern)
    except re.error as e:
        print(f"Invalid regular expression: {e}", file=sys.stderr)
        sys.exit(1)

    input_paths = args.files

    files_to_search: List[Union[str, Path]] = []

    # от URL?
    temp_dir = None
    if args.from_url:
        # създаваме временна директория
        tmp = tempfile.mkdtemp(prefix="mgrep_temp_")
        temp_dir = Path(tmp)
        # сваляме всички URL-и
        local = download_urls(input_paths, temp_dir)
        files_to_search = local
    else:
        # локална файлова система
        if args.recursive:
            files_to_search = gather_files_from_dirs(input_paths)
        else:
            files_to_search = [Path(p) for p in input_paths]

    try:
        run_multi_threaded(compiled, files_to_search,
                           is_in_memory=args.in_memory,
                           is_line_numbers=args.line_number,
                           amount_of_workers=args.parallel)
    except InvalidAmountOfWorkers as e:
        print(f"Invalid amount of workers: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # cleanup temp dir, ако има
        if temp_dir is not None:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

if __name__ == '__main__':
    main()
