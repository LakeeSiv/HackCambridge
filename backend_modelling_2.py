import math
import numpy as np
import matplotlib


def r(gender, height, mass, age):
    # This function will return the average r value to use to calculate concentration
    if gender == "male":
        r_value = 0.62544 + 0.13664 * height - mass * (0.00189 + 0.002425 / height ** 2) + (0.57986 + 2.545 * height -0.02255 * age) / mass
        return r_value
    elif gender == "female":
        r_value  = 0.50766 + 0.11165 * height - mass * (0.001612 + 0.0031 / height ** 2) - (0.62115 - 3.1665 * height) / mass
        return r_value

def plot_concentration(alcohol_ingested, half_life, height, mass, gender, interval=60): # ensure all units in seconds
    '''
    Function returns two numpy arrays. One of the time and the second of the blood alcohol concentration for that particular drink
    '''
    r = r(gender, height, mass, age)
    t = np.linspace(0,interval, 43200)
    # sets time interval
    c = np.linspace(0, interval, 43200)
    c = ((alcohol_ingested)*(1-((1/2)**(t/half_life))) - (0.018/3600)*t)

    plt.plot(c, t) 