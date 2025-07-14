
#Algorithm to read and plot Attocube NeasSNOM files from nano spectroscopy module
# thiago.santos@lnls.br 


#Importing libraries

#TK used to path dialog box
#Pandas used to import file and data handling
#Matplotlib used to plot data
#RE used to extract numbers from metadata header
#Scipy used to calculate FFT

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.fft import fft, fftfreq
#from scipy.fft import nufft, nufft_freq
from scipy.interpolate import interp1d

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
    O4A = df['O4A']

    #Phase with unwrap
    O0P = np.unwrap(df['O0P'])
    O1P = np.unwrap(df['O1P'])
    O2P = np.unwrap(df['O2P'])
    O3P = np.unwrap(df['O3P'])
    O4P = np.unwrap(df['O4P'])

    wnumber = df['Wavenumber'] #wavenumber vector


    #Ploting data:
    fig,(amplitude, phase) = plt.subplots(2,1)

    amplitude.plot(wnumber,O0A, label = 'O0A')
    amplitude.plot(wnumber,O1A, label = 'O1A')
    amplitude.plot(wnumber,O2A, label = 'O2A')
    amplitude.plot(wnumber,O3A, label = 'O3A')
    amplitude.plot(wnumber,O4A, label = 'O4A')
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

     print("Dataframe loaded.")

     #Preparing plot
     fig, (ax1,ax2,ax3) = plt.subplots(3, 1)
     fig.canvas.manager.set_window_title("Inteferograms File")

     #Geting interferograms

     #Calculating space domain in microns
     i=0
     space_domain = np.array([]) #create an empty list
     while i<pixelarea_z: #loop for each i index up to pixelarea_z length
        space_domain = np.hstack([space_domain, i*interferometer_distance/pixelarea_z]) #append to list an point sized with interferometer distance/point numbers
        i = i+1
     
     #Zero filling factor: times of interferogram length filled with zeros
     zf_factor = 4; 

     #Calculating reciprocal space domain length
     sampling_rate = 1 / (space_domain[1] - space_domain[0]) #  sampling rate in micrometers
     sampling_rate = (sampling_rate * 10000)/2 #Converting  sampling rate to centimeters
     reciprocal_domain_len = len(np.fft.fftfreq(len(space_domain), d=1/(sampling_rate)))

     i=0 #initializes counter for elements inside interferogram
     k=0 #initializers counter for interferograms

     interferograms_stack = np.empty((averaging+1,pixelarea_z+1)) # creating empty 2d array for interferograms (for future averaging)
     ffts_stack = np.empty((averaging+1,zf_factor*reciprocal_domain_len)) # creating empty 2d array for ffts with averaging+1 columns and reciprocal_domain_len lines
   
     #Geting interferogram elements and performing FFT for each one

     while k<averaging: #K is one interferogram
         interferogram = np.array([]) #reset interferogram vector
         while i<pixelarea_z:
            element_value_amplitude = O2A[i+k*pixelarea_z] #takes the interest element value from amplitude interferogram
            element_value_phase = O2P[i+k*pixelarea_z] #takes the interest element value from phase interferoram
            element_value = element_value_amplitude*np.cos(element_value_phase) #Calculates the real part from element value
            interferogram = np.hstack([interferogram, element_value]) #append element value to new interferogram
            interferograms_stack[k,i] = element_value #Append current element velue to all interferograms stack for interferogram averaging
            i = i+1 #adds to element in interferogram counter
         ax1.plot(space_domain,interferogram)
        

         k = k+1 #incremet of interferoram number
         i=0 #reset for element counter

         #DFT for single interferogram
         
         #Interpolating interferogram and removing DC component
         interferogram_AC = interferogram - np.mean(interferogram) # Removing DC component from interferogram
         interp1d_f = interp1d(space_domain, interferogram_AC) #Creates interpolated function relating space domain and interferogram amplitude
         space_domain_ip1d = np.linspace(space_domain.min(), space_domain.max(), len(space_domain)) #Creates equally spaced space_domain with same number of points from original, ip1d = interpolated
         interferogram_ip1d = interp1d_f(space_domain_ip1d) #Interpolates interferogram amplitude values for each point of equally spaced space domain, ip1d = interpolated

         #Windowing
         window = np.kaiser(len(interferogram_ip1d), 14) #Creating a kaiser window with same length as interferogram
         interferogram_ip1d = interferogram_ip1d*window #Aplying window to interferogram

         #Performing DFT
         interferogram_length = len(interferogram_AC)  #Taking interferogram length

         wnumber_domain = np.fft.fftfreq(zf_factor*interferogram_length, d = 1/(sampling_rate)) # taking reciprocal domain in cm-1
         fft_result = np.fft.fft(interferogram_AC,zf_factor*interferogram_length) #Taking fft from interferogram
         ffts_stack = np.vstack([ffts_stack, fft_result]) #append fft result to ffts stack

         ax2.plot(wnumber_domain[:zf_factor*interferogram_length//2],np.abs(fft_result)[:zf_factor*interferogram_length//2]) #append current fft amplitude from current interferogram to FFTs amplitude board
         ax3.plot(wnumber_domain[:zf_factor*interferogram_length//2],np.unwrap(np.angle(fft_result)[:zf_factor*interferogram_length//2])) #appent current fft phase from current interferogram to FFTs phase board
         print("Added FFT of interferogram ",k)

         
    # Converting Amplitude and Phase interferograms to real interferograms

     print("Interferograms loaded.")
     
     #Calculating average interferogram
     interferogram_average = np.empty((pixelarea_z)) #create an empty list for average values per position

     i=0 #Counter for element value in interferogram
     k=0 #Counter for interferogram number
     while i<pixelarea_z: #Loop to scal all elements in each interferogram
         while k<=averaging: #Loop to scan all interferograms i values
             element_value = element_value+interferograms_stack[k,i] #Appending of elements values to summation variable
             interferogram_average[i] = element_value #adds it to vector
             k = k+1
         interferogram_average[i] = element_value/averaging #Do the average by the number of interferograms
         element_value = 0 #Reset element value summation
         i=i+1 #increments element counter
         k = 0 #Reset interferogram counter to a new element averaging
     
     print("Average interferogram calculated.")
     
     #Ploting average interferogram
     average_plot, = ax1.plot(space_domain,interferogram_average, label = 'Average') #Appends average curve to graph
     average_plot.set_color('r') #chage the color to read
     average_plot.set_linewidth(2) #change thickness

     
     #FFT with numpy
     
     #Interpolating average interferogram
     interferogram_average_AC = interferogram_average - np.mean(interferogram_average) # Removing DC component from interferogram
     interp1d_f = interp1d(space_domain, interferogram_average_AC) #Creates interpolated function relating space domain and interferogram amplitude
     space_domain_ip1d = np.linspace(space_domain.min(), space_domain.max(), len(space_domain)) #Creates equally spaced space_domain with same number of points from original, ip1d = interpolated
     interferogram_average_ip1d = interp1d_f(space_domain_ip1d) #Interpolates interferogram amplitude values for each point of equally spaced space domain, ip1d = interpolated

     #Windowing
     #window = np.bartlett(len(interferogram_average_ip1d)) #Creating a bartlett window with same length as interferogram
     #window = np.hamming(len(interferogram_average_ip1d)) #Creating a hamming window with same length as interferogram
     window = np.kaiser(len(interferogram_average_ip1d), 14) #Creating a kaiser window with same length as interferogram
     interferogram_average_ip1d = interferogram_average_ip1d*window #Aplying window to interferogram

     
     #Performing DFT
     interferogram_length = len(interferogram_average_AC)  #Taking interferogram length
     sampling_rate = 1 / (space_domain[1] - space_domain[0]) #  sampling rate in micrometers
     sampling_rate = (sampling_rate * 10000)/2 #Converting  sampling rate to centimeters
       
     #Zero filling factor: times of interferogram length filled with zeros
     zf_factor = 4;

     wnumber_domain = np.fft.fftfreq(zf_factor*interferogram_length, d = 1/(sampling_rate)) # taking reciprocal domain in cm-1
     #fft_result = np.fft.fft(interferogram_average_AC) #Taking fft from interferogram
     fft_result = np.fft.fft(interferogram_average_AC,zf_factor*interferogram_length) #Taking fft from interferogram
     
     fft_amplitude = np.abs(fft_result) #Taking absolute to amplitude
     fft_phase = np.angle(fft_result) #Taking phase
     fft_phase = np.unwrap(fft_phase) #Unwraping phase
    

     #Ploting details
     ax1.legend()
     ax1.set_title('Interferograms')
     ax1.set_xlabel('Space [um]')
     ax1.set_ylabel('A.U.')
     ax1.grid(True)
     

     #ax2.imshow(interferograms_stack, extent = [space_domain[2],space_domain[pixelarea_z-2],0,averaging], cmap = 'inferno') #Colormap of interferograms stack
     
     
     #Plotting FFT
     average_fft_ampl_plot, = ax2.plot(wnumber_domain[:zf_factor*interferogram_length//2], fft_amplitude[:zf_factor*interferogram_length//2], label = 'Average') #Appends average fft to screen 2 plot
     average_fft_ampl_plot.set_color('r') #Set color red to curve
     average_fft_ampl_plot.set_linewidth(2) #Set width 2 to curve
     ax2.set_title('Amplitude FFT')
     ax2.set_xlabel('cm-1')
     ax2.set_ylabel('A.U.')
     ax2.grid(True)
     ax2.set_xlim(0,5000)
     ax2.set_xticks(range(0,5000,200))
     ax2.legend()

     average_fft_phase_plot, = ax3.plot(wnumber_domain[:zf_factor*interferogram_length//2], fft_phase[:zf_factor*interferogram_length//2], label = 'Average')
     average_fft_phase_plot.set_color('r')
     average_fft_phase_plot.set_linewidth(2)
     ax3.set_title('Phase FFT')
     ax3.set_xlabel('cm-1')
     ax3.set_ylabel('A.U.')
     ax3.grid(True)
     ax3.set_xlim(0,5000)
     ax3.set_xticks(range(0,5000,200))
     ax3.legend()

     plt.show()
     #plt.plot(fft_phase)
     #plt.show()
     
'''
This function will load a linescan from linescan file
'''
def load_linescan(file_path, data_start, averaging, pixelarea_z, scan_area_x):
    print("Load linescan function here!")

    #Loading file
    print("Loading linescan file")
    df = pd.read_csv(file_path, delim_whitespace = True, on_bad_lines='skip', header = data_start)
    print("Dataframe loaded\n")

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

    #wavenumber
    wavenumber = df['Wavenumber']

    #Taking values for O2

    i=0; #initializing element counter in the line
    k=0; #initializing number of lines counter
    l_scan = np.empty((0, 2*pixelarea_z)) #initializing 2d array with zero lines of 2*pixelarea length
    line_elements = np.array([]) #initializing an empty 1d array to get elements and append to 2d array

    while k <pixelarea_x: #loop for each full line
        while i<(2*pixelarea_z): #loop to take line elements
            element_value = O2A[(k*(2*pixelarea_z))+i] #Take the element number k*(2*pixelarea_z)+i, where k*(2*pixelarea_z) is the number of elements from other lines, i is the number of elements on current line
            line_elements = np.hstack([line_elements,element_value]) #Append the element to the current line array
            i = i+1 #add to element counter
        i=0 #Reset element counter
        l_scan = np.vstack([l_scan, line_elements]) #append current line to 2d array
        line_elements = np.array([]) #reset current line array
        k = k+1 #add to line counter

    # Ploting
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Linescan File")
    wnumber_limit = wavenumber[2*pixelarea_z-1] #Calculating wavenumber axis limit
    im = ax.imshow(l_scan, cmap = 'inferno', extent = [0,wnumber_limit,0,scan_area_x], aspect = 'auto' ,origin = 'lower')
    ax.set_title('Linescan')
    ax.set_xlabel('Wavenumber [cm-1]')
    ax.set_ylabel('Space [um]')
    plt.show()


#Main loop: to be possible to open another file when the first is closed

#Welcome message:

root = tk.Tk()
root.withdraw()

tk.messagebox.showinfo("sSNOM File Reader", "sSNOM File Reader: It opens .txt files from sSNOM and shows its content. Supported Files: spectra, interferograms, linescans")

root.destroy()

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

        if header[i].lower().startswith('# scan area'): #check if scanned starts with scanned starts with scan area
            scan_area_x = float(re.findall(r"[-+]?\d+\.\d+",header[i])[0]) #take X from first element of vector of taken int numbers
            scan_area_y = float(re.findall(r"[-+]?\d+\.\d+",header[i])[1]) #take Y from second element of vector of taken int numbers
            scan_area_z = float(re.findall(r"[-+]?\d+\.\d+",header[i])[2]) #take Z from third element of vector of taken int numbers

        i = i+1
    print("Detected averaging : ",averaging)
    print("Pixel Area X: ", pixelarea_x)
    print("Pixel Area Y: ", pixelarea_y)
    print("Pixel Area Z: ", pixelarea_z)
    print("Interferometer center : ", interferometer_center," um")
    print("Interferometer distance : ", interferometer_distance," um")
    print("Scan Area X: ",scan_area_x, "um")
    print("Scan Area Y: ",scan_area_y, "um")
    print("Scan Area Z: ",scan_area_z, "um")

    #Checking file tyoe:
    if "Depth" in header[data_start]:
        print("Interferogram file detected")
        load_interferograms(file_path, data_start, averaging, pixelarea_z, interferometer_distance)
    elif (((scan_area_x>0) and (scan_area_y == 0) and (scan_area_z == 0)) or ((scan_area_x==0) and (scan_area_y > 0) and (scan_area_z == 0)) or ((scan_area_x == 0) and (scan_area_y == 0) and (scan_area_z > 0))):
        print("Linescan file detected")
        load_linescan(file_path, data_start, averaging, pixelarea_z, scan_area_x)
    else:
        print("Spectra file detected")
        load_spectra(file_path)

