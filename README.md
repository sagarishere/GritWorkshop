
# GritWorkshop README

Welcome to the GritWorkshop! In this workshop, you'll get hands-on experience with developing a target function to drive a car's behavior in a simulated environment. Below are the steps to get started, followed by a brief description of the task.

## INSTALL INSTRUCTIONS

### Getting the Repo

To get started, you first need to download the repository:

```bash
git clone https://github.com/KimGrip/GritWorkshop.git
cd GritWorkshop
```

### Setting Up Python

If you haven't already, [install Python](https://www.python.org/downloads/). As of this workshop, Python 3.11 is supported.

### Installing pip

If your Python installation didn't come with pip (Python's package installer), [here's a guide](https://pip.pypa.io/en/stable/installation/) on how to install it.

### Required Libraries

> fastest way would be
>
> ```bash
>   pip install -r requirements.txt
> ```

This workshop relies on a couple of Python libraries. You can install them using the following commands:

```bash
    pip install pygame neat-python
```

### Running the Workshop Files

To run the Python files, navigate to the directory containing the file in the terminal or command prompt and use the following command:

```bash
python filename.py
```

If you're using VSCode, you can also run the Python file by right-clicking and selecting "Run Python File in Terminal."

## Task Description

### Objective

Your main objective in this workshop is to design a `TARGET_FUNCTION`. This function will essentially determine how the car behaves in its environment. Think of it as the brain of the car - you decide what the car thinks is important and what it should aim for.

### The Car and Its Components

The simulated car has a few key attributes:

- **POSITION**: Represents the car's location in the 2D environment.
- **VEL**: The current velocity of the car.
- **ROTATION**: The direction in which the car is currently facing.
- **RAYCASTS**: These are "sensors" that detect obstacles. They emanate from the car and provide feedback on nearby objects.

### Modifying the Target Function

Your main task will be to modify the `TARGET_FUNCTION.py` file. This is where you will shape the behavior of the car.

### Need Help?

If you encounter any issues or have questions, please don't hesitate to come to me. I'm here to help!

---

2D Racing game for the gritlab workshop made By Kim Gripenberg

Big Thanks to Lucas Chang for his art contributions:
<https://www.artstation.com/kruske>
