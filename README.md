# Crash Prediction

TODO Introduction


## Installation

On jupyter.nesi.org.nz, open a terminal and clone this repository:
```
git clone https://github.com/neon-ninja/crash_prediction.git
```
then change directory:
```
cd crash_prediction
```
and use the Makefile to install dependencies and create a conda environment:
```
make venv_nesi
```

If you are using this code on a regular computer (not HPC), make sure you have:
- [Git](https://git-scm.com/downloads),
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed,
- [JupyterLab](https://jupyter.org/install.html) or another program to run
  notebooks,
- the `make` command.

Then clone this repository, for example from a terminal using:
```
git clone https://github.com/neon-ninja/crash_prediction.git
```
change directory and install all dependencies using `make`:
```
cd crash_prediction
make venv
```

Whichever way you installed the code, now you can run the provided notebooks
using the `crash_prediction` kernel.


## Getting Started

First, you need to retrieve the CAS dataset, using the `cas_data` script:
```
cas_data download data/cas_dataset.csv
```

Then prepare the dataset, i.e. select relevant colums, filter NaN values, etc.:
```
cas_data prepare data/cas_dataset.csv -o results/cas_dataset.csv
```

TODO explain other scripts and notebooks


## Documentation

TODO link to pages below and generated API documentation if any


## License

This project is published under the MIT License. See the [LICENSE](LICENSE) file
for details.


## Contact

If you have any question or comment on this work, do not hesitate to contact us:

- Nick Young (nick.young@auckland.ac.nz) from the [Center for eResearch](https://www.eresearch.auckland.ac.nz/),
- Maxime Rio (maxime.rio@nesi.org.nz) from [NeSI](https://www.nesi.org.nz/).
