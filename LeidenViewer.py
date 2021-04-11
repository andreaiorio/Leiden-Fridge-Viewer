import matplotlib.pyplot as plt
import pandas as pd
import glob, os
from datetime import datetime

class LeidenFridge:
    
    def __init__(self, file_or_folder, dateformat='%Y-%m-%d %H:%M:%S'):  
        
        def _open_df(file):
            '''Return a pandas dataframe from Leiden log file'''
            return pd.read_csv(file, 
                               skiprows=[0,1], 
                               delimiter='\t', 
                               index_col=0,  
                               header=[0,1,2], 
                               date_parser=lambda date: datetime.strptime(date, dateformat))
        
        try:
            '''Open single log file'''
            self.df = _open_df(file_or_folder)

        except:
            '''Try to open directory'''
            try:
                _files = glob.glob(file_or_folder + '/*.dat')
                self.df = _open_df(_files[0])
                
                for _file in _files[1:]:
                    try : self.df = pd.concat([self.df, _open_df(_file)]).drop_duplicates()
                    except: pass 
            except:
                raise('Failed to open file or directory.')
            
        self.T = self.df[['T0','T1','T2','T3','T4','T5','T6','T7','T8','T9']]
        self.R = self.df[['R0','R1','R2','R3','R4','R5','R6','R7','R8','R9']]
        self.heaters = self.df[['I0', 'I1', 'I2', 'I3']]
        self.T_names = self.T.columns.get_level_values(level=1).to_list()
        self.T_calibrations = self.T.columns.get_level_values(level=2).to_list()
    
    def plot(self, channels=range(10)):
        _T_channels = ['T{}'.format(_c) for _c in channels]
        return self.T[_T_channels].plot(figsize=(10,6))

    def plot_interactive(self):
        import ipywidgets as widgets
        fig, ax = plt.subplots(figsize=(10, 6))
        t_list = ["T{}".format(i) for i in range(10)]
        checkbox = [widgets.Checkbox(description=_t) for _t in t_list]

        @widgets.interact(**{c.description: c.value for c in checkbox})
        def _update(**kwargs):
            ax.clear()
            for (key,value) in kwargs.items():
                if value: self.T[key].plot(ax=ax)
        return fig, ax
    
    def last_T(self):
        return self.T.tail(1)