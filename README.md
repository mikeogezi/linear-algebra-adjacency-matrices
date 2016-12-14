# mth-204-linear-algebra-adjacency-matrices
I wrote this code to read a json file that contains the names of people along with their friends. An adjacency matrix and graph diagram are then computer from the data.  I then compute the eigenvalues, eigenvectors, frobenius norm, trace e.t.c of the matrix and display them.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisities

What things you need to install the software and how to install them

```
1. python (https://python.org)
```

### Installing

A step by step series of examples that tell you have to get a development env running

**Linux and Windows**
To use this software you'll need to install *matplotlib*, *numpy* and *networkx* after installing *python*
```
Type these into your terminal/command-line
$ pip install matplotlib
$ pip install numpy
$ pip install networkx

To read from the *data.json* file and generate it's graph and resulting adjacency matrix  
$ python index.py
```

**Format of JSON file**

How the JSON file should be written so that the program can read it properly.

* Inside the data object we have the person's department
* In the department we have the person's name along with an array of the names of his friends

```
"data": {
  "computer_science": {
    "Michael": ["David", "Daniel", "Tobi"]
  }
}
```

## Built With

* Atom
* Python
* Numpy
* Matplotlib
* NetworkX

## Authors

* **Michael Ogezi**

See also the list of [contributors](https://github.com/okibeogezi/mth-205-linear-algebra-adjacency-matrices/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
