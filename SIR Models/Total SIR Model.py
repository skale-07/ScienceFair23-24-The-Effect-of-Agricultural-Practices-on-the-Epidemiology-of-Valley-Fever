#imports
from scipy.integrate import odeint #used for differential equations
import matplotlib.pyplot as plt #used for graphing
import numpy as np #using for graphing
import csv #used for exporting data to CSV

#parameters
N = 1000000  #assumed total population for modeling
I0 = 1       #initial number of infected individuals
R0 = 0       #initial number of recovered individuals
S0 = N - I0  #number of susceptible individuals at the start (everyone else)
beta0 = 0.20 #baseline dust transmission rate (%)
gamma = 1/21 #recovery rate (assuming an average of 21 days to recover)

#dust sensor readings in ug/m^3
dust_readings = {
    "Control": 0.6945606695, 
    "Organic Material Cover": 0.1311018131,
    "Mulch": 0.07670850767,
    "Salt Brine": 0.1408647141,
}

#SIR model differential equations
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

#initial conditions vector
y0 = S0, I0, R0

#a grid of time points (in days)
t = np.linspace(0, 150, 150)  #simulate for 150 days

#plot setup
plt.figure(figsize=(10, 6))

#dictionary for max cases per day
max_casesTuple = {} #raw cases tuple with (cases, day)
max_cases = {} #raw cases value

#dictionary for average cases
avg_cases = {}

#dictionary for percent efficiency
percent_effDict = {}

#iterating over each dust reading and plotting
for label, dust_reading in dust_readings.items():
    
    #multiply by amplication factor to amplify change in beta due to dust readings
    amplification_factor = 5
    
    #adjust beta based on dust reading
    beta = beta0 * (1 + amplification_factor * (dust_reading / dust_readings["Control"]))

    #integrate the SIR equations over the time grid, t
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    #plot the data using time, cases, and scenarios (labels)
    plt.plot(t, I, label=label)

    #find (max cases, day) and raw cases
    max_cases_day = np.argmax(I)
    max_cases_value = I[max_cases_day]
    max_cases[label] = round(max_cases_value, 3)
    max_casesTuple[label] = (round(max_cases_day, 3), round(max_cases_value, 3))
    
    #find (average cases, scenario)
    avg_cases_value = np.mean(I)
    avg_cases[label] = round(avg_cases_value, 3)

for scenario, values in max_cases.items():
    
    #calculate percent decrease by dividing max cases per scenario by max cases for control
    if scenario != "Control" in max_cases.keys():
        
        percent_eff = round((((max_cases["Control"] - max_cases[scenario])/max_cases["Control"]) * 100), 3) # (control cases - scenario cases)/(control cases) * 100        
        
        #add to dictionary and print
        percent_effDict[scenario] = percent_eff
        print(f"The percent decrease of {scenario} compared to the control is {percent_eff}%.")

#print average cases for extra data to confirm model works (if average cases is similar for each scenario then model makes sense due to epidemiology)
#print out necessary data        
for scenario, values in max_casesTuple.items():
    print(f"The max cases caused by {scenario} is {values[1]} on day {values[0]}.")
    
for scenario, values in avg_cases.items():
    print(f"The average cases when {scenario} is used is {values}.")


#send percent efficiency to csv file
with open('Percent Decrease.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
            
    #write header 
    writer.writerow(['Agricultural Practices', 'Percent Efficiency'])

    #automate creation of data table for percent efficiency
    for scenario, value in percent_effDict.items():
        writer.writerow([scenario, str(value)])

#send max cases to csv file 
with open('Max Cases.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    
    #write header
    writer.writerow(['Agricultural Practices', 'Day', 'Max Cases'])
    
    for scenario, values in max_casesTuple.items():
        writer.writerow([scenario, str(values[0]), str(values[1])])
  
# Adding labels and title to the plot
plt.xlabel('Time (days)')
plt.ylabel('Number of Infected Individuals')
plt.title('Impact of Different Dust Readings on Valley Fever Infections')
plt.legend()
plt.show()