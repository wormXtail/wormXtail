# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:09:44 2022

@author: Nedelcu Liviu
"""
# Sinewave analyser v1.1, made with Streamlit

import streamlit as st
import numpy as np
import pandas as pd
import scipy as sp

def singleToneAnalyser():
    
    st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",  
    page_title='Sinewave Simulator • Streamlit', 
    page_icon=None
    )
    st.sidebar.header("""Wave Simulator""")
    st.sidebar.write("""_created by Liviu Nedelcu_ :smile:""")
    st.sidebar.markdown("""<br>""", True)
    
    st.sidebar.header(""" Plot Type""")
    
    option = st.sidebar.radio(
        'Signals',
        ('Signal Only', 'Noise Only', 'With Noise'))
    
    option_chart = st.sidebar.radio(
        'Graphics',
        ('Line', 'Area'))
    
    st.sidebar.header(""" PARAMETERS """)
    
    amplitude = st.sidebar.number_input("Amplitude",0.0,10.0,1.0,0.01)
    
    fstep = st.sidebar.selectbox("Frequency Step",['100','10','5','1','0.1','0.01'])
    fstep = float(fstep)
    freq = st.sidebar.slider("Frequency (Hz)",0.0,1000.0,1.0,fstep)

    dstep = st.sidebar.selectbox("Time Step",['100','10','5','1','0.1','0.01'])
    dstep = float(dstep)
    duration = st.sidebar.number_input("Duration (s)",0.0,3600.0,1.0,dstep)
    

    pstep = st.sidebar.selectbox("Phase Step (pi coefficient)",['0.66','0.5','0.33','0.25','0.15','0.125','0.05','0.005'])
    pstep = float(pstep)
    phase = st.sidebar.number_input("Phase",-2*np.pi,2*np.pi,0.0,pstep*np.pi)
    
    noise_level = st.sidebar.number_input("Noise Level",0.0,10.0,0.1,0.01)

    sample_rate = st.sidebar.selectbox("Sample Rate", ['500','1000','12000','24000','44100','48000','128000','192000','Other'])
    if sample_rate == 'Other':
        numinput = st.sidebar.number_input("Choose your own sample rate",0,6000000,44100,1)
        samprate = numinput
        st.sidebar.write(samprate)
    elif sample_rate != 'Other':
        samprate = int(sample_rate)
    

    time = np.linspace(0.0,float(duration),samprate)
    y = amplitude*np.sin(2*np.pi*freq*time + phase)
    z = noise_level*np.sin(2*np.pi*30*freq*time + phase)
    noise = np.random.normal(0.0,noise_level,samprate)
    signal = y + noise
    
    chart_signal = pd.DataFrame(y, time)
    chart_noise = pd.DataFrame(noise, time)
    chart_signoise = pd.DataFrame(signal, time)

    if freq <= samprate/2:
        if option_chart == 'Line':
            if option == 'Signal Only':
                st.line_chart(chart_signal, use_container_width=True, height=500)
            elif option == 'Noise Only':
                st.line_chart(chart_noise, use_container_width=True, height=500)
            elif option == 'With Noise':
                st.line_chart(chart_signoise, use_container_width=True, height=500)
        elif option_chart == 'Area':
            if option == 'Signal Only':
                st.area_chart(chart_signal, use_container_width=True, height=500)
            elif option == 'Noise Only':
                st.area_chart(chart_noise, use_container_width=True, height=500)
            elif option == 'With Noise':
                st.area_chart(chart_signoise, use_container_width=True, height=500)        
    elif freq < 0 or samprate <= 0 or freq >= samprate/2:
        st.error('Sample rate must be at least 2 times greater than maximum Frequency')

if __name__ == '__main__':
    singleToneAnalyser()
