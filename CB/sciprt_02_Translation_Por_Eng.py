import os 
import httpx
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from googletrans import Translator
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
##########################################################
##########################################################
#### Action of Description
translator = Translator() 

# Patch googletrans to skip SSL verify
translator.client = httpx.Client(verify=False)
###########################################################
OS_ID_stop_Fil            = [] 
timestamp_Fil             = []
employee_id_Fil           = []
assembly_Fil              = []
subassembly_Fil           = []
component_Fil             = []
failure_type_Fil          = []
action_Fil                = []
description_of_action_Fil = []
###########################################################
Non_type_IDs    = []
Original_text   = [] 
Translated_Text = []
for i6 in range(len(description_of_action)): # len(description_of_action) 11240,11250
    temp  = str(description_of_action[i6]) 
    tempC = temp.split(" ") 

    if len(tempC) > 1 and len(tempC) < 40:
        try:
            result = translator.translate(temp, src='pt', dest='en')
            ##############################
            Original_text.append(temp) 
            Translated_Text.append(result.text)
            #######################################
            OS_ID_stop_Fil.append(OS_ID_stop[i6])
            timestamp_Fil.append(timestamp[i6])
            employee_id_Fil.append(employee_id[i6])
            assembly_Fil.append(assembly[i6])
            subassembly_Fil.append(subassembly[i6])
            component_Fil.append(component[i6])
            failure_type_Fil.append(failure_type[i6])
            action_Fil.append(action[i6])
            #######################################
        except Exception as e :
            Non_type_IDs.append(i6)
        # print(type(temp))
    if (i6 % 500) == 0:
        print("Processing row:", i6)
################################
        df = pd.DataFrame({
            'S.No' : np.arange(len(Original_text)).tolist(),
            'OS_ID_stop':OS_ID_stop_Fil,
            'timestamp':timestamp_Fil,
            'employee_id':employee_id_Fil,
            'assembly':assembly_Fil,
            'subassembly':subassembly_Fil,
            'component':component_Fil,
            'failure_type':failure_type_Fil,
            'action':action_Fil,
            'Original Text': Original_text,
            'Translated Text': Translated_Text
        }) 

        df.to_excel('Translated_Data.xlsx', index=False)
######################################################
######################################################


# result = translator.translate("Olá, como vai você?", src='pt', dest='en')
# print(result.text)  # Output: Hello, how are you?








