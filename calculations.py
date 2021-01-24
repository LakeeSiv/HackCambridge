"""


we want a function that takes lists of
alcoholic drink,
time,
volume,

example list (firstlist)

 [[vodka, 11:00, 10], [beer, 12:00, 100]]

then it returns a list of
time
Blood alcohol level over time

example (secondlist)

t= [11:00,11:30,12:00]
BAC = [0.01,0.005,0.2]

we also want to take in the age, height, weight
"""

"""
f(firstlist, age, height, weight)
    return secondlist



"""
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt





empty_stomach_half_life_hour = 0.1066
full_stomach_half_life_hour = 0.3009

#Alcohol and their percentages which is later used in the alcohol_ingested_function
alcohol_dictionary = {"Cider": 6, "Beer": 6, "Lager": 4, "Red Wine": 12.5, "White Wine": 11, "Vodka": 40, "Whiskey": 40, "Rum": 40, "Units. Enter the number of units in volume": 0}

def r(gender, height, mass, age):
    '''
    This function calculates the r-value based on the user which is used to calculate the concentration
    '''
    if gender == "male":
        r_value = 0.62544 + 0.13664 * height - mass * (0.00189 + 0.002425 / (height ** 2)) + (0.57986 + 2.545 * height -0.02255 * age) / mass
        return r_value
    elif gender == "female":
        r_value  = 0.50766 + 0.11165 * height - mass * (0.001612 + 0.0031 / height ** 2) - (0.62115 - 3.1665 * height) / mass
        return r_value

def alcohol_ingested(percentage, volume):
    '''
    This function returns the amount of alcohol consumed by the user based on the type of alcohol and the volume consumed
    '''

    alcohol_units = percentage * volume / 1000
    mass_of_alcohol = 8 * alcohol_units
    return mass_of_alcohol

def plot_concentration(alcohol_ingested, half_life, height, mass, age, gender, interval=60):
    '''
    Function returns two numpy arrays. One of the time and the blood alcohol concentration for that particular drink.
    Every drink has their own graph. The theory behind the model states that the individual graphs can be superimposed to give one main graph detailing
    the user's blood concentration levels
    The time interval of 60 is a default. It means that the calculations are done for each minute. This is done to reduce computational time and can be adjusted as required.
    '''
    r_value = r(gender, height, mass, age)
    print(r_value)
    t = np.arange(0,24*3600*1.5, interval)

    c = ((alcohol_ingested)/(r_value*mass))*(1-((1/2)**(t/half_life))) -(0.018/3600)*t
    # The function due to its nature will continue being negative due to its mathematical form. However in reality, all concentrations must be non - negative.
    placeholder = 0
    for i in range(0,len(c)):
        if c[i] < 0:
            break
        else:
            placeholder += 1

    c[placeholder:] = 0
    return t,c

def main_calculate(user_info, drinks_list):

    '''
    The user_unfo will be list of variables arranged as such
    user_info = [gender, age, weight, height, eater_or_not]
    The drinks will be a list of lists represented as such:
    drinks_list = [["vodka", "11:00", 10], ["beer", "12:00", 100]]
    Then based on where the user has eaten or not, an appropriate half life is chosen
    '''
    gender, age, mass, height, eaten = user_info
    user_r_value = r(gender, height, mass, age)

    if eaten == "Yes":
        half_life_in_seconds = full_stomach_half_life_hour * 3600
    else:
        half_life_in_seconds = empty_stomach_half_life_hour * 3600

    t = np.arange(0, 3* 24 * 3600, 60)
    c= np.zeros(len(t))

    # The above are the main time and concentration arrays. The concentration array of each drink will be superimposed on the concentration array above.
    start_time = drinks_list[0][1]
    # The drinks will be arranged in time order with the earliest drink being first
    start_time_dt = datetime.strptime(start_time, "%H:%M") # The time will be in the format as such: "11:00". It is convert to a datetime for ease of calculation
    # This will be the start time of the drinking
    for drink in drinks_list:
        percent,time_string, volume = drink

        time_dt = datetime.strptime(time_string, "%H:%M")
        print(time_dt)
        time_diff =  time_dt - start_time_dt 
        print(time_diff)
        time_seconds = time_diff.seconds

        # The time seconds doesn't apply to the first drink but applies to subsequent drinks, their time after the first drink is needed for superimpostion

        alcohol_ingested_amount = alcohol_ingested(percent, volume)
        drink_time, drink_concentration = plot_concentration(alcohol_ingested_amount, half_life_in_seconds,
                                                             height, mass, age, gender)
        drink_time_alternate = drink_time + time_seconds
        # Line above gets the time and concentration ready to be added to the main time and concentration
        # All calculations are done in seconds, however for faster calculations, we have chosen the time interval between calculations to be 60 seconds.
        # Will now need to add the concentration onto the main concentration array while taking care of the time difference between drinking
        # print(drink_time)
        # print( drink_concentration)
        # print(drink_time_alternate)
        # print("time_seconds", time_seconds)
        # plt.plot(drink_time, drink_concentration)
        # plt.show()
        len_concentration = len(drink_concentration)
        for i in range(0, len_concentration):
            c[i + time_seconds // 60]  += drink_concentration[i]
    return t, c



# user_info = ["male", 18, 70, 1.60, "No"]
# drinks_list = [["Vodka", "11:00", 50], ["Beer", "13:00", 500], ["Beer", "23:59", 500]]

# time, concentration = main_calculate(user_info, drinks_list)
# plt.plot(time, concentration)
# plt.show()