from scipy.integrate import odeint  # used for differential equations
import matplotlib.pyplot as plt  # used for graphing
import numpy as np  # used for graphing
import csv  # used for exporting data to CSV
import pandas as pd  # used for data manipulation

# parameters
N = 100000000  # assumed total population for modeling
I0 = 1  # initial number of infected individuals
R0 = 0  # initial number of recovered individuals
S0 = N - I0  # number of susceptible individuals at the start (everyone else)
gamma = 1 / 21  # recovery rate (assuming an average of 21 days to recover)

# baseline dust transmission rates (%)
beta0 = {
    "beta_3D" : 0.011 * 20,
    "beta_3G" : 0.0165 * 20,
    "beta_3E" : 0.013 * 20,
    "beta_3A" : 0.02 * 20,
    "beta_2A" : 0.2365 * 20,
} 
# Dust readings for each location and agricultural practice
dust_readings = {
    "3D": {
        "Control": 19.74236388,
        "Organic Material Cover": 1.601593625,
        "Mulch": 2.852,
    },
    "3G": {
        "Control": 3.42483660,
        "Organic Material Cover": 1.91333333,
        "Mulch": 1.94540613,
    },
    "3E": { 		
        "Control": 15.78486056,
        "Organic Material Cover": 0.55365474,
        "Mulch": 2.41145140,
    },
    "3A": {
        "Control": 7.994861823,
        "Organic Material Cover": 9.496679947,
        "Mulch": 7.351394422,
    },
    "2A": {
        "Control": 4.725099602,
        "Organic Material Cover": 1.320053121,
        "Mulch": 3.15936255,
    },
}

amplification_factor = 1

# SIR model differential equations
def deriv(y, t, N, beta, gamma):
    """
    Calculate the derivatives of the SIR model.

    Parameters:
    - y: tuple of floats (S, I, R)
        The current values of the susceptible, infected, and recovered populations.
    - t: float
        The current time.
    - N: float
        The total population size.
    - beta: float
        The transmission rate.
    - gamma: float
        The recovery rate.

    Returns:
    - tuple of floats (dSdt, dIdt, dRdt)
        The derivatives of the susceptible, infected, and recovered populations.
    """
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# initial conditions vector
y0 = S0, I0, R0

# a grid of time points (in days)
t = np.linspace(0, 225, 225)  # simulate for 150 days



for location, scenarios in dust_readings.items():
    plt.figure(figsize=(10, 6))  # Create a new figure for each location

    daily_cases_data = []  # Empty list to collect daily cases data
    max_cases_data = []  # Empty list to collect max cases data
    control_dust = scenarios["Control"]  # Dust reading for the control scenario

    # Iterate over each scenario and dust value for the current location
    for scenario, dust_value in scenarios.items():
        
        # Adjust beta using the calculated reduction factor, ensuring it's reduced
        beta = beta0[f"beta_{location}"] * (1 + amplification_factor * (dust_value) / control_dust)
        print(f"beta for {location} {scenario}: {beta}")
            
        # Integrate the SIR equations over the time grid, t
        ret = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T

        # Collect daily case data for the CSV
        for day, cases in enumerate(I):
            daily_cases_data.append([scenario, day + 1, round(cases, 2)])
        
        #find (max cases, day) and raw cases        
        max_cases_day = np.argmax(I)
        max_cases_value = round(I[max_cases_day], 3)
        max_cases_data.append([scenario, max_cases_day, max_cases_value])
        
        # Plot the data
        plt.plot(t, I, label=scenario)

    # Customize and display the plot for the current location
    plt.xlabel('Time (days)')
    plt.ylabel('Number of Infected Individuals')
    plt.title(f'Impact of Dust Reduction Interventions on Valley Fever Infections at {location}')
    plt.legend()
    plt.show()
    
    # Write the max cases data to a CSV file for the current location
    print(f"Max cases data for {location}: {max_cases_data}")    
    csv_filename = f'C:\\Users\\skale\\OneDrive\\Desktop\\Science Project Data\\Future Experimentation\\max_cases_{location}.csv'
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Agricultural Practice', 'Day', 'Max Cases'])
        writer.writerows(max_cases_data) 
        
        
    # Write the collected data to a CSV file for the current location
    csv_filename = f'C:\\Users\\skale\\OneDrive\\Desktop\\Science Project Data\\Future Experimentation\\cases_{location}.csv'
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Agricultural Practice', 'Day', 'Cases'])
        writer.writerows(daily_cases_data)

