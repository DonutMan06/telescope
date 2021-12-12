![telescope_1](https://github.com/DonutMan06/DonutMan06/blob/main/tel01.png)

# Telescope simulator

This is a little Python GUI that highlights the effect of different parameters of a Newton's telescope, among which :

- the diameter of the primary mirror
- the focal length of the primary mirror
- the focal length of the ocular
- the apparent field of view of the ocular

The user can than selects a target (Mars, Jupiter, Saturn or the Moon) and all any relevant informations will be printed on the middle and right pannels.

If the user clicks on the `Plot` button, a picture of the ocular will be displayed on a (I hope) WYSISYG mode. Just keep in mind that the apparent field (shown in black) should be equal to the apparent field you set on the left pannel.

![telescope_2](https://github.com/DonutMan06/DonutMan06/blob/main/tel02.png)

This is somehow similar to the [online tool provided by Stelvision](https://www.stelvision.com/astro/simulateur-de-telescope/) but with a lot more informations.

## Installation

Clone this project and create a new Python virtual environment, activate it and install the dependancies of this project (mainly scientific stuff like numpy, matplotlib and pyqt)

```
$ python -m venv /path/to/virtualenv/
$ source /path/to/virtualenv/bin/activate
$ cd /path/to/telescope/
$ pip install -r requirements.txt
```

## Usage

You just have to execute the `telescope.py` script. The user interface is really simple and does not need any documentation.

## Known limitations and issues

- the orbit of the different targets are all circular (no excentricity and the mean radius is derived from the aphelia and perihelia parameters). This is a limitation that need to be kept in mind but since I only wanted a rought estimate of what kind of observation may be exepected, this is not big deal. An update here should not be very difficult to implement.

- the photometric parameters are all derived from precise mathematics expressions and are expected to be really accurate (wrt the relative distance between Earth and the target and the target's albedo). Nevertheless, the apparent magnitude still need some improvements. For this same reason, the apparent magnitude seen in the ocular is not yet implemented.

- all the computations are done inside the mainwin class : even if the code runs, the design should be highly improved by doing these computations outside the class definition
