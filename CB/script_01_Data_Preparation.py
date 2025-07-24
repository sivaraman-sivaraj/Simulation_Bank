import os 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
#######################################################
#######################################################
# File_List = 0

# ### Set the folder path containing the Excel files
# folder_path = "/home/z0150218/Downloads/Chatbot_Real/Sumara_Data"

# ### List all Excel files in the folder
# xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# ### Loop through each Excel file and read data
# for file_name in xlsx_files:
#     file_path = os.path.join(folder_path, file_name)
    
#     try:
#         # Read the Excel file (default is the first sheet)
#         df = pd.read_excel(file_path)
#         print(f"\nContents of '{file_name}':")
#         print(df.head())  # Print first few rows
#     except Exception as e:
#         print(f"Error reading '{file_name}': {e}")
##########################################################
##########################################################
Data       = pd.read_excel("Sumara_Data/translated_registroCausaRaiz.xlsx") 

OS_ID_stop            = Data["OS_ID_stop"].tolist() 
timestamp             = Data["timestamp"].tolist()
employee_id           = Data["employee_id"].tolist()
assembly              = Data["assembly"].tolist()
subassembly           = Data["subassembly"].tolist()
component             = Data["component"].tolist()
failure_type          = Data["failure_type"].tolist()
action                = Data["action"].tolist()
description_of_action = Data["description_of_action"].tolist()
###############################################################
# print(len(OS_ID_stop))
# print(len(action),len(employee_id),len(assembly),len(subassembly),len(component),len(failure_type),len(action),len(description_of_action)) 
#################################################
#################################################
### Observing the Unique Assembly 
Unique_Assembly = [] 
for i in range(len(assembly)):
    temp = assembly[i] 
    if temp not in Unique_Assembly:
        Unique_Assembly.append(temp) 
print("The number of unique Assembly :",len(Unique_Assembly))
#################################################
#################################################
### Observing the subassembly
Unique_subassembly = [] 
for i2 in range(len(assembly)):
    temp = subassembly[i2] 
    if temp not in Unique_subassembly:
        Unique_subassembly.append(temp) 
print("The number of unique Sub-Assembly :",len(Unique_subassembly)) 
#################################################
#################################################
### Observing the unique component 
Unique_Component = [] 
for i3 in range(len(component)):
    temp = component[i3] 
    if temp not in Unique_Component:
        Unique_Component.append(temp) 
print("The number of unique Component :",len(Unique_Component)) 
#################################################
#################################################
### Unique failure type 
Unique_failure_type = [] 
for i4 in range(len(failure_type)):
    temp = failure_type[i4]
    if temp not in Unique_failure_type:
        Unique_failure_type.append(temp) 
print("The number of unique failure type :",len(Unique_failure_type)) 
#################################################
################################################# 
#### Unique action 
Unique_action = [] 
for i5 in range(len(action)):
    temp = action[i5] 
    if temp not in Unique_action:
        Unique_action.append(temp) 
print("The number of Unique actions to fix :",len(Unique_action))
#################################################
################################################# 
#### Action of Description
Unique_Action_Description = [] 
count = 0
for i6 in range(len(description_of_action)):
    temp = str(description_of_action[i6]) 
    temp = temp.split(" ")
    if len(temp) > 3:
        print(temp)
        count += 1 

print("The number of empty count :", count)

#################################################
#################################################