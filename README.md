# Solver for Letter Boxed

This is a solver for the New York Times [Letter Boxed puzzle](https://www.nytimes.com/puzzles/letter-boxed). 
Uses the NLTK word list as the default dictionary. Outputs all possible solutions.

## Requirements

* `pip install -r requirements.txt`

## Usage

* `lb.py -h` for help
* `lb.py -t|--top <letters> -l|--left <letter> -b|--bottom <letters> -r|--right <letters>` to solve the puzzle
* Optional parameters:
  * `-m|--min <int>` to specify the minimum word length (default: 4)
  * `-x|--max <int>` to specify the maximum word length (default: no limit)
  * `-d|--depth <int>` to specify the search depth (default: 4)

## Example
> `lb.py -t ihy -l aws -b ern -r ftl -m 4 -x 6 -d 3`
```
1. ['afaint', 'theist', 'twirly']
2. ['fains', 'syrtis', 'shewel']
3. ['faint', 'theist', 'twirly']
...
41. ['wish', 'hearth', 'hafnyl']
42. ['wisha', 'anarya', 'afetal']
43. ['first', 'theat', 'twinly']
```
![Example solution](sample_solution.png)

## License
Licensed under the Apache License Version 2.0.


