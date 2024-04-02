import pandas as pd 
import matplotlib.pyplot as plt

# Paths to the max cases CSV files for each location
file_paths = {
    "2A": r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\max_cases_2A.csv",
    "3A": r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\max_cases_3A.csv",
    "3D": r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\max_cases_3D.csv",
    "3E": r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\max_cases_3E.csv",
    "3G": r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\max_cases_3G.csv"
}


# Initialize a DataFrame to store percent decrease across all locations
percent_decrease_all = pd.DataFrame()

for location, file_path in file_paths.items():
    # Load the data
    max_cases = pd.read_csv(file_path)
    
    # Calculate percent decrease from the control
    control_max_cases = max_cases[max_cases['Agricultural Practice'] == 'Control']['Max Cases'].iloc[0]
    max_cases['Percent Decrease'] = (((control_max_cases - max_cases['Max Cases']) / control_max_cases) * 100)
    max_cases['Location'] = location  # Add location information
    
    print("Location" + str(max_cases))
    
    # Append to the combined DataFrame
    percent_decrease_all = pd.concat([percent_decrease_all, max_cases], ignore_index=True)

# Save the compiled data to a new CSV file
percent_decrease_all.to_csv(r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\percent_decrease.csv", index=False)

# Load the percent decrease data
percent_decrease = pd.read_csv(r"C:\Users\skale\OneDrive\Desktop\Science Project Data\Future Experimentation\percent_decrease.csv")

# Unique locations
locations = percent_decrease['Location'].unique()

for location in locations:
    # Filter the data for the current location
    data = percent_decrease[percent_decrease['Location'] == location]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(data['Agricultural Practice'], data['Percent Decrease'], color='skyblue')
    plt.xlabel('Agricultural Practice')
    plt.ylabel('Percent Decrease from Control (%)')
    plt.title(f'Percent Decrease in Max Cases by Agricultural Practice for {location}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

