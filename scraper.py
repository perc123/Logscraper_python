#!/usr/bin/env python
# coding: utf-8

# In[21]:


import re
import os

def add_txt_extension(file_name):
    # Check if the file_name has an extension, and if not, add '.txt'
    if not file_name.endswith('.txt'):
        file_name += '.txt'
    return file_name

def extract_log_info(log_file, output_file_name):
    log_data = []
    application_launch_count = 0
    software_version = None
    warning_states = []
    error_states = []
    crashes = []

    # Check if the path exists
    if not os.path.exists(log_file):
        print("File not found. Please try again.")
        return

    with open(log_file, 'r') as file:
        log_lines = file.readlines()

    # Search the file for the specific information
    for line in log_lines:
        log_data.append(line.strip())
        if "Application launched" in line:
            application_launch_count += 1
        elif "Software version" in line:
            software_version = re.search(r'\d+\.\d+\.\d+', line).group()
        elif "Error: Application exit due to critical failure" in line:
            error_states.append(line)
            crash_date = re.search(r'\d{4}-\d{2}-\d{2}', line).group()
            crash_time = re.search(r'\d{2}:\d{2}:\d{2}.\d{6}', line).group()
            crashes.append({'date': crash_date, 'time': crash_time})
        elif "Error" in line:
            error_states.append(line)
        elif "Warning" in line:
            warning_states.append(line)

    output_file_name = add_txt_extension(output_file_name)  # Ensure the output file has a '.txt' extension

    # Check if the new file name already exists in the directory
    while os.path.exists(output_file_name):
        user_input = input(f"The file '{output_file_name}' already exists. Do you want to overwrite it? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        elif user_input.lower() == 'no':
            output_file_name = input("Enter a new name for the output file: ")
            output_file_name = add_txt_extension(output_file_name)  # Ensure the new name has a '.txt' extension
        else:
            print('Only yes or no please.')

    # Write the extracted information to the specified output file
    with open(output_file_name, 'w') as output_file:
        output_file.write(f"Software Version: {software_version}\n")
        output_file.write(f"Application Launched {application_launch_count} times\n")

        if error_states:
            output_file.write("Error States:\n")
            for error in error_states:
                output_file.write(error + '\n')

        if warning_states:
            output_file.write("Warning States:\n")
            for warning in warning_states:
                output_file.write(warning + '\n')

        if crashes:
            output_file.write("Crashes:\n")
            for crash in crashes:
                output_file.write(f"Crash occurred on {crash['date']} at {crash['time']}\n")
        
    print(f"Log data written to '{output_file_name}'.")

if __name__ == "__main__":
    while True:
        log_file = input("Enter the path to the log file, or type 'exit' to exit the application: ")
        if log_file.lower() == 'exit':
            break

        output_file_name = input("Enter the name of the output file: ")
        extract_log_info(log_file, output_file_name)


# In[ ]:




