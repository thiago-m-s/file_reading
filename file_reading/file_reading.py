
#Algorithm to read and plot Attocube NeasSNOM files from nano spectroscopy module
# thiago.santos@lnls.br 


#Importing libraries

#TK used to path dialog box
#Pandas used to import file and data handling
#Matplotlib used to plot data
#RE used to extract numbers from metadata header

import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

#Initialization disclaimers


print('****************************************************************************************************************')
print('*                                               sSNOM data visualizer                                          *')
print('*              This aplication plots an .txt spectra and/or interferogram file from Attocube sSNOM             *')
print('*                                      thiago.santos@lnls.br Imbuia Group                                      *')
print('****************************************************************************************************************\n\n')
print('Supported files: Not normalized spectra, normalized spectra, interferograms')



    

#Defining function to load normalized files
def load_spectra(file_path):

    print("Loading spectra file")

    df = pd.read_csv(file_path, delim_whitespace = True, on_bad_lines='skip', skiprows = data_start)

    print("Dataframe loaded\n")

    #Amplitudes
    O0A = df['O0A']
    O1A = df['O1A']
    O2A = df['O2A']
    O3A = df['O3A']
    O3A = df['O4A']

    #Phase with unwrap
    O0P = np.unwrap(df['O0P'])
    O1P = np.unwrap(df['O1P'])
    O2P = np.unwrap(df['O2P'])
    O3P = np.unwrap(df['O3P'])
    O4P = np.unwrap(df['O4P'])

    wnumber = df['Wavenumber'] #wavenumber vector


    #Ploting data:
    fig,( amplitude, phase) = plt.subplots(2,1)

    amplitude.plot(wnumber,O0A, label = 'O0A')
    amplitude.plot(wnumber,O1A, label = 'O1A')
    amplitude.plot(wnumber,O2A, label = 'O2A')
    amplitude.plot(wnumber,O3A, label = 'O3A')
    amplitude.plot(wnumber,O3A, label = 'O4A')
    amplitude.legend()
    amplitude.set_xlim(0,3000)
    amplitude.set_title('Amplitude')
    amplitude.set_xlabel('Wavenumber [cm-1]')
    amplitude.set_ylabel('A.U')
    amplitude.set_xticks(np.arange(0,3000,100))
    amplitude.grid(True)


    phase.plot(wnumber, O0P, label = 'O0P')
    phase.plot(wnumber, O1P, label = 'O1P')
    phase.plot(wnumber, O2P, label = 'O2P')
    phase.plot(wnumber, O3P, label = 'O3P')
    phase.plot(wnumber, O4P, label = 'O4P')
    phase.set_xlim(0,3000)
    phase.legend()
    phase.set_xticks(np.arange(0,3000,100))
    phase.set_title('Phase')
    phase.set_xlabel('Wavenumber [cm-1]')
    phase.set_ylabel('rad')
    phase.grid(True)

    plt.show()



'''
This function will read number of interferograms (averaging), number of points and starting data line to stack interferograms to plots
'''
def load_interferograms(file_path, data_start, averaging, pixelarea_z, interferometer_distance):


     #Loading file
     print("Loading interferogram file")
     df = pd.read_csv(file_path, delim_whitespace = True, on_bad_lines='skip', header = data_start)
     print("Dataframe loaded\n")

     #Stacking interferograms to 

     #Amplitudes
     O0A = df['O0A']
     O1A = df['O1A']
     O2A = df['O2A']
     O3A = df['O3A']
     O4A = df['O4A']

     #Phase with unwrap
     O0P = np.unwrap(df['O0P'])
     O1P = np.unwrap(df['O1P'])
     O2P = np.unwrap(df['O2P'])
     O3P = np.unwrap(df['O3P'])
     O4P = np.unwrap(df['O4P'])

     #Depth
     depth = df['Depth']
     k=0
     i=0

     print(depth)

     #Preparing plot

     ax = plt.gca() #Get the current axes: it shares plot axes to append curves

     #Geting interferograms

     '''
     Pending: Create x axis vector with micrometer values done
     Append interferogram to interferograms 2d array
     Calculate average interferogram
     Calculate FFT for each interferogram and apend to FFTs
     Calculate average FFT
     '''

     #Calculating space domain in microns
     i=0
     space_domain = np.array([]) #create an empty list
     while i<pixelarea_z: #loop for each i index up to pixelarea_z length
        space_domain = np.hstack([space_domain, i*interferometer_distance/pixelarea_z]) #append to list an point sized with interferometer distance/point numbers
        i = i+1


     i=0
     while k<averaging: #K is one interferogram
         interferogram = np.array([]) #reset interferogram vector
         while i<pixelarea_z:
            element_value = O2A[i+(k*pixelarea_z)] #takes the interest element value
            i = i+1 #increment to element number counter
            interferogram = np.hstack([interferogram, element_value]) #append element value to new interferogram
         ax.plot(space_domain,interferogram) #append curve to plot
         k = k+1 #incremet of interferoram number
         i=0 #reset for element counter

     #Ploting details
     plt.title('Interferograms')
     plt.xlabel('Space [um]')
     plt.ylabel('A.U.')
     plt.grid(True)
     plt.show()
               

#Main loop: to be possible to open another file when the first is closed



while 1==1:

    

    #selecting file path

    def file_dialog():
        file_path = filedialog.askopenfilename(
            title = "Select your .txt spectra file"
         )
        return file_path

    file_path = file_dialog()
    print("File path: ", file_path, "\n")


    #Detection of Header
    '''
    It scans for .txt file looking for lines starting with #
    It adds to a counter for each line with # considering data starts in the following without #
    data_start is the line that doesnt contain #, where data begins

    It is necessary because normalized and not normalized files contain diferent head lengths

    It copies the header text in order to get metadata

    It also takes the columns names line in order to check file tyoe (interferogram, spectra etc). It does it taking also lines starting with zero number
    '''

    i=0

    header = []

    with open(file_path,"r") as pre_ds:

        for i, line in enumerate(pre_ds):
            if line.strip().lower().startswith("#") or line.strip().lower().startswith("row"):

                data_start = i
                header.append(line.strip())


    print(header)

    #Reading file with pandas
    # df = dataframe
    #The delimiter is space, and 30 first lines are skipped

    print("\nData starts in line number", data_start)


    #Taking metadata
    '''
    Headers metadata acquiring:

    Averaging: number of interferograms in the file
    Pixel Area: 
        X = pixels in space
        Y = pixels in spce
        Z = number of interferogram points
    '''

    i=0

    #Taking averaging
    while i<(data_start+1): #plus one is the line with columns names
        print(header[i].strip()) #scans header
        if header[i].lower().startswith("# averaging"): #check if the scanned starts with averaging
            averaging = int(re.findall(r"\d+",header[i])[0]) #extract numbers for the line and converts to integer
        
        if header[i].lower().startswith("# pixel area"): #check if scanned starts with pixel area
            pixelarea_x = int(re.findall(r"\d+",header[i])[0]) #take X from first element of vector of taken int numbers
            pixelarea_y = int(re.findall(r"\d+",header[i])[1]) #take Y from second element of vector of taken int numbers
            pixelarea_z = int(re.findall(r"\d+",header[i])[2]) #take Z from third element of vector of taken int numbers

        if header[i].lower().startswith('# interferometer'): #check if scanned starts with interferometer
            interferometer_center = float(re.findall(r"[-+]?\d+\.\d+",header[i])[0]) # take interferometer center position from vector of taken int numbers of i th line converting from string to float
            interferometer_distance = float(re.findall(r"[-+]?\d+\.\d+",header[i])[1]) # take interferometer distance from vector of taken int numbers of i th line converting from string to float

        i = i+1
    print("Detected averaging : ",averaging)
    print("Pixel Area X: ", pixelarea_x)
    print("Pixel Area Y: ", pixelarea_y)
    print("Pixel Area Z: ", pixelarea_z)
    print("Interferometer center : ", interferometer_center," um")
    print("Interferometer distance : ", interferometer_distance," um")

    #Checking file tyoe:
    if "Depth" in header[data_start]:
        print("Interferogram file detected")
        load_interferograms(file_path, data_start, averaging, pixelarea_z, interferometer_distance)
    else:
        print("Spectra file detected")
        load_spectra(file_path)

