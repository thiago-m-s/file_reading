
#Algorithm to read and plot Attocube NeasSNOM files from nano spectroscopy module
# thiago.santos@lnls.br 


#Importing libraries

#TK used to path dialog box
#Pandas used to import file and data handling
#Matplotlib used to plot data

import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Initialization disclaimers

print('*******************************************************************************************')
print('*                                  sSNOM data visualizer                                  *')
print('*              This aplication plots an .txt spectra file from Attocube sSNOM             *')
print('*                           thiago.santos@lnls.br Imbuia Group                            *')
print('*******************************************************************************************')


#selecting file path

def file_dialog():
    file_path = filedialog.askopenfilename(
        title = "Select your .txt spectra file"
        )
    return file_path

file_path = file_dialog()
print(file_path)

#Reading file with pandas
# df = dataframe
#The delimiter is space, and 30 first lines are skipped
df = pd.read_csv(file_path, delim_whitespace = True, on_bad_lines='skip', skiprows = 30)

print("Dataframe loaded\n")

#Creating data from harmonic channels, calling by column name

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



