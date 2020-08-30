<div align="center">

<img src="./images/word-search-logo.jpg" width="50%" alt="Word Search Generator Logo" />

# Word Search Generator

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

Generate a random word search and key using a list of words.

- [Quick Start](#quick-start)
- [Customization](#customization)
- [GNU GPL 3.0 License](./LICENSE)
- [Roadmap](#roadmap)

## Quick Start

Word Search Generator allows you to create a word search in one of two
languages and output it to a variety of formats.

1. Create a text file. On the first line enter the dimensions of the
   word search separated by a space. **width height**.

```
15 15
```

2. Specify a language on the next line.

| code | language |
| ---- | -------- |
| en   | English  |
| de   | Deutsch  |

```
15 15
de
```

3. Add the words for your word search, each on a separate line.

```
15 15
de
hut
schirm
handtuch
ball
bikini
sonnencreme
sand
getränk
wasser
sonnenbrille
buch
```

4. Install dependencies. Word Search Generator requires [Python 3](https://www.python.org/downloads/).

bash

```bash
cd ./word-search-generator
python3 -m pip install -r requirements.txt
```

powershell/cmd

```powershell
cd .\word-search-generator
py -3 -m pip install -r requirements.txt
```

5. Generate the word search.

bash

```bash
cd ./word-search-generator
cat path/to/my-text-file | python3 ./src/word-search-generator.py
```

powershell/cmd

```powershell
cd .\word-search-generator
type path\to\my-text-file | py -3 .\src\word-search-generator.py
```

output

```Board
B I K I N I T O K Z G F Ä H
H F C S S L L Ö F I I J ẞ Z
Q P G ẞ R U P E V S Y Ü C C
R Q X E B A L L E F X W F Ä
F Z W C S O N N E N C R E M
W M W Q G W A S S E R Ü D J
Ö M Z T A H T S A N D B Ä K
L R D R U S O F D H P C Z Z
K E Ü S S C H I R M U W N G
Y R S C I R X D V B U C H ẞ
S N C U D G E T R Ä N K H E
Ü M J R M B P G T D Ö ẞ U J
C H I C S F Z A Z N M J T A
H A N D T U C H N X Ä X A O
Ü Q F J L G Z Ä O O M B L Y
```

Happy Searching!

## Customization

Checkout all available options using the `--help` command.

```bash
usage: word-search-generator.py [-h] [-k] [--language {en,de}] [-c] [-o OUTPUT]

Generate a word search from stdin

optional arguments:
  -h, --help            show this help message and exit
  -k, --key             Generate a word search and its key
  --language {en,de}    Choose a language for the word search
  -c, --csv             Return data as csv. Defaults to False. Save to file with -o.
  -o OUTPUT, --output OUTPUT
                        Output to file. Specifies the folder name and partial filename. Ex: -o ./out -> ./out/out_word_search.txt Defaults to stdout.
```

### Key

Getting the word search key is as simple as adding the `--key` argument.

bash

```bash
cd ./word-search-generator
cat path/to/my-text-file | python3 ./src/word-search-generator.py --key
```

powershell/cmd

```powershell
cd .\word-search-generator
type path\to\my-text-file | py -3 .\src\word-search-generator.py  --key
```

output

```Board
Key
          W
          A
          S
  B U C H S       S A N D
          E             S
          R             O
                        N
                        N
                        E B
H                       N A
U       H A N D T U C H C L
T                       R L
  S O N N E N B R I L L E
            B I K I N I M
      G E T R Ä N K     E

Board
T S F D E W Y ẞ C I Z Z M V
N D ẞ C K A T T J Ä R C V V
Y B K T P S I P D B M E X Ö
P B U C H S W E S S A N D K
J M Ä E C E H E B X L W S B
Z J T P J R D E V D P A O W
T C V N Z R Y U Z P X Y N W
Ä B B X Ü O B X H Q L U N K
K X M D U A O S F W J X E B
H C B J E J U I N G Y E N A
U A B Ü H A N D T U C H C L
T Q Ü Q F C Z T B D Z L R L
F S O N N E N B R I L L E J
D M Ä L K I B I K I N I M E
Ö P K G E T R Ä N K E I E K
```

### Language

You can override the language that is specified in the text file by using
the `--language` flag.

bash

```bash
cd ./word-search-generator
cat path/to/my-text-file | python3 ./src/word-search-generator.py --language en
```

powershell/cmd

```powershell
cd .\word-search-generator
type path\to\my-text-file | py -3 .\src\word-search-generator.py --language en
```

### Output

You can customize the output location and format using commandline arguments.

| location | details                                                  | flag                                       |
| -------- | -------------------------------------------------------- | ------------------------------------------ |
| stdout   | Default. Prints your key and board to the console window | None                                       |
| file     | Writes your key and board to separate files              | -o [folder name] OR --output [folder name] |

| format | details                                                                  | flag        |
| ------ | ------------------------------------------------------------------------ | ----------- |
| spaces | Default. Separates characters with spaces                                | None        |
| csv    | Separates characters with commas. You can import this into a spreadsheet | -c OR --csv |

#### Outputting the board to a csv file

bash

```bash
cd ./word-search-generator
cat path/to/my-text-file | python3 ./src/word-search-generator.py --csv --output ./data
```

powershell/cmd

```powershell
cd .\word-search-generator
type path\to\my-text-file | py -3 .\src\word-search-generator.py --csv --output .\data
```

output

```
word-search-generator
  /data
    data_word_search.csv
```

## Roadmap

Here's a list of feature that could be implemented.

### Save Options

- pdf
- svg
- other image file

### UX

- Build web interface
- Using web interface allow playing the websearch.
- Using web interface allow sharing of word searches via link
- Using web interface allow info blob on word discovery - here's a set
  of links or defintions in a card like fashion.
- Allow backwards words
- Allow diagonal words

### Other

- Convert codebase to Rust and target WASM
- Convert codebase to JavaScript and run just in browser
- Add test suite
