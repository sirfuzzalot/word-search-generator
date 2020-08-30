"""
Generates a word search from a list of words.
"""
# Copyright (C) 2020 Tom Saunders

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import time
import string
import random
import argparse
from collections import deque

import numpy


def run_generator_from_stdin(use_key=False, use_csv=False, folder=None, language=None):
    """Gets data from stdin and then creates a word search"""
    raw_data = _ingest_stdin()
    dimensions = _get_dimensions(raw_data)
    lang = _get_language(raw_data)
    if language:
        lang = language
    words = _get_words(raw_data)

    key, board = generate_word_search(words, lang, dimensions)
    options = {
        "use_key": use_key,
        "output": "file" if folder else "stdout",
        "folder": folder,
        "use_csv": use_csv,
    }
    _export(board, key, dimensions, options)


def _ingest_stdin() -> list:
    """Ingest data from stdin"""
    if sys.stdin.buffer:
        with sys.stdin.buffer as stdin_handler:
            return stdin_handler.read().decode().splitlines()
    else:
        with sys.stdin as stdin_handler:
            return stdin_handler.read().splitlines()


def _get_dimensions(raw_data: list) -> tuple:
    """Get the width and height of the word search"""
    dimension_list = raw_data[0].split(" ")
    if len(dimension_list) != 2:
        raise ValueError(
            "Header containing word search dimensions is invalid. Correct usage - Ex: 2 12"
        )
    try:
        width = int(dimension_list[0])
        height = int(dimension_list[1])
    except ValueError:
        raise ValueError(
            "Width and Height in Header must be integers. Ex: 2 4"
        ) from None
    return (width, height)


def _get_language(raw_data: list) -> str:
    """Get the language of the word search"""
    lang = raw_data[1]
    return lang


def _get_words(raw_data: list) -> list:
    """Gets a list of words"""
    return raw_data[2:]


def generate_word_search(words: list, lang: str, dimensions: tuple) -> tuple:
    """Generate the word search"""
    if not isinstance(words, list):
        raise ValueError("words must provide a list of words")
    for word in words:
        if not isinstance(word, str):
            raise ValueError("Each word in words must be a string")
    if not isinstance(lang, str):
        raise ValueError("lang must provide a valid language string")
    if not isinstance(dimensions, (tuple, list)):
        raise ValueError(
            "dimensions must provide a tuple of integers. ex: (width, height)"
        )
    for dimension in dimensions:
        if not isinstance(dimension, int):
            raise ValueError("dimension in dimensions must be an integer")
    _validate_word_length(words, dimensions)
    character_set = _get_lang_characters(lang)
    words = _conform_characters(words)
    key, board = _run_simulation(words, character_set, dimensions)
    return key, board


def _validate_word_length(words: list, dimensions: tuple) -> None:
    """Validate character counts against dimensions"""
    max_characters = dimensions[0] * dimensions[1]
    for word in words:
        if len(word) > dimensions[0] and len(word) > dimensions[1]:
            raise ValueError(
                "Length of word is greater than the dimensions provided: "
                + f"{word} - {dimensions}"
            )


def _conform_characters(words: list) -> list:
    """Uppercase all letters"""
    return [word.upper() for word in words]


def _get_lang_characters(lang: str) -> list:
    """Get the language specific character set"""
    if lang == "en":
        return string.ascii_uppercase
    elif lang == "de":
        return string.ascii_uppercase + "ẞÄÖÜ"


def _run_simulation(words: list, character_set: str, dimensions: tuple,) -> numpy.array:
    """Simulate the word search board"""
    board, repeat_counter = _wipe_board(words, dimensions)
    queue = deque(words)
    spinner = deque([" / ", "- -", " \\ ", " | "])
    while queue:
        word = queue.pop()
        progress = spinner.pop()
        sys.stdout.write(f"\r{progress}")
        spinner.appendleft(progress)
        if not _added_word(word, dimensions, board):
            repeat_counter[word] += 1
            if repeat_counter[word] > 5:
                board, repeat_counter = _wipe_board(words, dimensions)
                queue = deque(words)
                time.sleep(0.01)
            else:
                queue.appendleft(word)
    sys.stdout.write(f"\r   \n")
    key = _render_whitespace(board.copy())
    board = _render_noise(character_set, board, dimensions)
    return key, board


def _wipe_board(words: list, dimensions: tuple) -> tuple:
    """Get Fresh numpy array and repeat counter"""
    board = _get_empty_board(dimensions)
    repeat_counter = {word: 0 for word in words}
    return board, repeat_counter


def _get_empty_board(dimensions: tuple) -> numpy.array:
    """Instantiate the board"""
    width = dimensions[0]
    height = dimensions[0]
    arr = numpy.full(width * height, fill_value=None).reshape(width, height)
    return arr


def _added_word(word: str, dimensions: tuple, board: numpy.array) -> bool:
    """Simulate adding word to board. True if added"""
    start_point = _choose_start_point(dimensions)
    direction = _choose_direction()
    end_point = _get_end_point(word, direction, start_point)
    if _detected_edge_collision(dimensions, end_point):
        return False
    if _detected_word_collision(word, direction, board, start_point):
        return False

    _save_word(word, direction, start_point, board)
    return True


def _choose_start_point(dimensions: tuple) -> tuple:
    """Picks a random point to start the word"""
    x = random.randrange(0, dimensions[0])
    y = random.randrange(0, dimensions[1])
    return x, y


def _choose_direction() -> str:
    """Pick a direction for the word"""
    return random.choice(["down", "right"])


def _get_end_point(word: str, direction: str, start_point: tuple) -> tuple:
    """Get the endpoint for word, direction and start point"""
    x, y = start_point
    length = len(word)
    if direction == "right":
        return x + length - 1, y
    elif direction == "down":
        return x, y + length - 1


def _detected_edge_collision(dimensions: tuple, end_point: tuple,) -> bool:
    """Detects if word collides with edge of board"""
    x2, y2 = end_point
    width, height = dimensions
    if x2 <= width - 1 >= 0 and y2 <= height - 1 >= 0:
        return False
    return True


def _detected_word_collision(
    word: str, direction: str, board: numpy.array, start_point: tuple
) -> bool:
    """Detects if word collides with another word"""
    x, y = start_point
    for increment, character in enumerate(word):
        if direction == "right":
            cell = board[x + increment][y]
            if not cell:
                continue
        elif direction == "down":
            cell = board[x][y + increment]
            if not cell:
                continue
        else:
            raise ValueError(f"direction not supported: {direction}")
        if cell != character:
            return True
    return False


def _save_word(
    word: str, direction: str, start_point: tuple, board: numpy.array
) -> None:
    """Saves the word's position"""
    x, y = start_point
    for increment, character in enumerate(word):
        if direction == "right":
            board[x + increment][y] = character
        elif direction == "down":
            board[x][y + increment] = character


def _render_whitespace(board: numpy.array) -> numpy.array:
    """Substitute None for whitespace"""
    return numpy.where(board == None, " ", board)


def _render_noise(
    character_set: str, board: numpy.array, dimensions: tuple
) -> numpy.array:
    """Substitute whitespace for random letters"""
    for row in range(dimensions[1]):
        for column in range(dimensions[0]):
            if not board[row][column]:
                board[row][column] = random.choice(character_set)
    return board


def _export(
    board: numpy.array, key: numpy.array, dimensions: tuple, options: dict = {}
) -> None:
    """Export the board to a variety of outputs"""
    defaults = {"use_key": False, "output": "stdout", "folder": None, "use_csv": False}
    config = {**defaults, **options}
    if config["output"] == "stdout":
        if config["use_key"]:
            print("Key")
            _send_to_stdout(key, dimensions, config["use_csv"])
            print("")
        print("Board")
        _send_to_stdout(board, dimensions, config["use_csv"])
    elif config["output"] == "file":
        if not os.path.exists(config["folder"]):
            os.makedirs(config["folder"], exist_ok=True)

        extension = "csv" if config["use_csv"] else "txt"
        if config["use_key"]:
            key_filename = os.path.join(
                config["folder"],
                f"{os.path.basename(config['folder'])}_key.{extension}",
            )
            _write_to_file(key, dimensions, key_filename, config["use_csv"])
        board_filename = os.path.join(
            config["folder"],
            f"{os.path.basename(config['folder'])}_word_search.{extension}",
        )
        _write_to_file(board, dimensions, board_filename, config["use_csv"])


def _send_to_stdout(
    board: numpy.array, dimensions: tuple, use_csv: bool = False
) -> None:
    """Send board, row by row to stdout"""
    for row in range(dimensions[1]):
        row_string = ""
        for column in range(dimensions[0]):
            row_string += f"{board[row][column]}{',' if use_csv else ' '}"
        print(row_string[:-2])


def _write_to_file(
    board: numpy.array, dimensions: tuple, filename: str, use_csv: bool = False
) -> None:
    """Send board, row by row to stdout"""
    with open(filename, "wb+") as file:
        for row in range(dimensions[1]):
            row_string = ""
            for column in range(dimensions[0]):
                row_string += f"{board[row][column]}{',' if use_csv else ' '}"
            try:
                row = f"{row_string}\n".encode()
                file.write(row)
            except UnicodeEncodeError:
                print(row_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a word search from stdin")
    parser.add_argument(
        "-k", "--key", action="store_true", help="Generate a word search and its key"
    )
    parser.add_argument(
        "--language",
        action="store",
        choices=["en", "de"],
        help="Choose a language for the word search",
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="store_true",
        help="Return data as csv. Defaults to False. Save to file with -o.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        help="Output to file. Specifies the folder name and partial "
        + "filename. Ex: -o ./out -> ./out/out_word_search.csv Defaults to stdout.",
    )
    args = parser.parse_args()
    run_generator_from_stdin(
        use_key=args.key, language=args.language, use_csv=args.csv, folder=args.output
    )
