"""
Modelling the alcohol
"""
empty_stomach_rate_per_hour = 6.5
empty_stomach_half_life_hour = 0.1066
full_stomach_rate_per_hour = 2.3
full_stomach_half_life_hour = 0.3009

#Alcohol and their percentage
alcohol_dictionary = {"Cider": 6, "Beer": 6, "Lager": 4, "Red Wine": 12.5, "White Wine": 11, "Vodka": 40, "Whiskey": 40, "Rum": 40, "Units. Enter the number of units in volume": 0}

def r(gender, height, mass, age):
    # This function will return the average r value to use to calculate concentration
    if gender == "male":
        r_value = 0.62544 + 0.13664 * height - mass * (0.00189 + 0.002425 / height ** 2) + (0.57986 + 2.545 * height -0.02255 * age) / mass
        return r_value
    elif gender == "female":
        r_value  = 0.50766 + 0.11165 * height - mass * (0.001612 + 0.0031 / height ** 2) - (0.62115 - 3.1665 * height) / mass
        return r_value

def concentration_superimpose():
    pass

def alcohol_ingested(alcohol_name, volume):
    '''
    This function returns the amount of alcohol consumed by the user based on the type of alcohol and the volume 
    ''''
    if alcohol_name == "Units. Enter the number of units in volume":
        mass_of_alcohol = 8 * volume # This isn't volume but rather the number of units
        return mass_of_alcohol

    else:
        percentage =  alcohol_dictionary[alcohol_name]
        alcohol_units = percentage * volume / 1000
        mass_of_alcohol = 8 * alcohol_units
        return mass_of_alcohol


