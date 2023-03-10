#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 00:09:27 2020

@author: nathan
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

class fip_plots():
    def __init__(self, freq_radday = np.ones(1),
                       fips = np.ones(1)):
    
        #Peaks of the smoothed lasso solution
        self.omega_peaks = None  # frequency of the peaks
        self.peakvalues = None # height of the peaks
        self.mlog10fip =  -np.log10(fips) 
        self.omegas = freq_radday 
        self.fips = fips
        self.periods = 2*np.pi/freq_radday 
        self.starname =  ''   
        self.ltip = np.log10(1-fips)

        self.fiplevel = None
        self.truepos = None
        self.bernouilli_unc = None
            
    def find_peaks(self):
        '''
        define the peaks appearing in the smoothed solution
        solution: their frequencies self.omega_peaks
        their values self.peakvalues, and decreasing order
        self.indexsort
        '''
        i = 0

        peakpos = []
        Nomegas = len(self.omegas)
        
        while i<Nomegas-1:
            if self.mlog10fip[i] >1e-2:
                j = i
                while self.mlog10fip[i] >1e-2 and i<Nomegas-1:
                    i = i+1
                array = self.mlog10fip[j:i]
                peakpos1 = j+np.argmax(array)
                peakpos.append(peakpos1)
            i = i+1

    
        peakvals = self.mlog10fip[peakpos]
        indexsort = np.argsort(-peakvals)
        peakpos = np.array(peakpos)
        peakpos_sort = peakpos[indexsort]
        
        if len(peakpos_sort)>0:
            self.omega_peaks = self.omegas[peakpos_sort]
            self.peakvalues = self.mlog10fip[peakpos_sort]
        else:
            self.omega_peaks = []
            self.peakvalues = []
            
            

    def plot_clean(self,number_highlighted_peaks_in,
                   starname = '',
                   fip_orientation = 'up',
                   annotations='periods',
                   marker_color = (0.85,0.325,0.098),
                   title = 'default',
                   save = False,
                      **kwargs): 
        ''' 
        Plot the FIP periodogram with highlighted highest peaks
        INPUTS:
            - number_highlighted_peaks_in: number of peaks to highlight
            - annotations: labels of the peaks 
            annotations is either set to a key of the 
            dictionary self.significance, and then corresponds to the
            significance of the highlighted peaks or to 'periods',
            in which case it shows the peak periods
            - marker_color: color of the marhers that highlight the 
            highest peaks
            - title: plot title
            - save: saves a pdf file if set to True
        '''
        #start_time = time.time()
        
        self.find_peaks()
        self.starname = starname
        
        nmaxpeaks = len(self.omega_peaks)
        number_highlighted_peaks = min(number_highlighted_peaks_in,nmaxpeaks)
        if number_highlighted_peaks_in >  nmaxpeaks:
            print('There are only', nmaxpeaks, 'peaks')
            
        peakvalues_plot = self.peakvalues[:number_highlighted_peaks]
        
        if title=='default':
            fipperio_title = self.starname + ' ' + 'FIP periodogram'
        else:
            fipperio_title = title
        
        if len(self.omega_peaks[:number_highlighted_peaks])>0:
            periods_plot = 2*np.pi/self.omega_peaks[:number_highlighted_peaks]
        else:
            periods_plot =[]
        

        bm = (0,0.447,0.741)
        gr = (0.2,0.4,0.)
        rr = (0.6,0.,0.6)#(0.8,0.447,0.741)
        gy = (0.9290,0.6940,0.1250)
        rm = (0.85,0.325,0.098)
        
        #fig = plt.figure(figsize=(10, 4))

        if number_highlighted_peaks>0:
            periods_maxpeaks = periods_plot
        maxperiod = self.periods[0]


        fig, ax1 = plt.subplots(figsize=(10, 4))
        colorfip = bm
        colortip = gy
        ax2 = ax1.twinx()   
        ax2.set_ylabel('$\log_{10}$ TIP', 
                       color=colortip,fontsize=18)
     
        ax2.semilogx(self.periods,self.ltip, alpha=0.7,
                     color = colortip,  
                     linewidth=3,zorder=-1)

        ylim2 = ax2.get_ylim()
        ax2.set_ylim([ylim2[0],0])        
        
        if fip_orientation == 'up':
            ax1.plot(self.periods, self.mlog10fip, 
                     linewidth=1.7
                     , color=colorfip
                     , rasterized = True)
            ax1.set_ylim([0, np.max(self.mlog10fip)*1.15])
            ax1.set_ylabel(r'-$\log_{10}$ FIP', 
                       fontsize=18, color=colorfip)
            ax1.set_zorder(ax2.get_zorder()+1)
            ax1.patch.set_visible(False)     
        
        else:
            ax1.plot(self.periods, -self.mlog10fip, 
                     linewidth=1.7
                     , color=colorfip
                     , rasterized = True)
            ax1.set_ylim([np.min(-self.mlog10fip)*1.15,0]) 
            ax1.set_ylabel(r'$\log_{10}$ FIP', 
                       fontsize=18, color=colorfip)
            peakvalues_plot = - peakvalues_plot
                
        #axes = plt.gca()               
        minP = min(self.periods)
        maxP = max(self.periods)
        ax1.set_xlim([minP,maxP])
            
        ylim = ax1.get_ylim()
        deltaY = ylim[1] - ylim[0]
        deltaX = np.log10(maxP) - np.log10(minP)

        if number_highlighted_peaks>0:
            
            if annotations is None:
                point_label=''          
            elif annotations=='periods':
                point_label = 'Peak periods (d)'
            elif annotations in self.significance.keys():
                point_label = annotations
            else:
                raise Exception(('The annotations key word '
            'has to be a key of the self.significance dictionary '
            'or ''periods'' or None'))
                
            #Cleaner outputs for standard significance evaluations
            if annotations=='log10faps':
                point_label = r'$\log_{10}$' + ' FAPs'
            if annotations=='log_bayesf_laplace':
                point_label = r'$\log$' + ' Bayes factor'
            if annotations=='log10_bayesf_laplace':
                point_label = r'$\log_{10}$' + ' Bayes factor'            
            
            ax1.plot(periods_maxpeaks, 
                     peakvalues_plot,'o',
                     markersize=5, color=marker_color,
                     label = point_label)
        
        
        y_legend = np.zeros(number_highlighted_peaks)
        x_legend = np.zeros(number_highlighted_peaks)

        for j in range(number_highlighted_peaks):
            
            if annotations=='periods':
                per = periods_maxpeaks[j]   
                p = str(per)
                indexpoint = p.find('.')
                if indexpoint<3:
                    ndigits = 4
                else:
                    ndigits =   indexpoint
                per = round(per, ndigits - indexpoint)
                p = str(per)
                annotation = p[:ndigits]
                
            elif annotations is not None:
                if j < len(self.significance[annotations]):
                    annotation = sci_notation(self.significance[annotations][j], decimal_digits=1, 
                                     precision=None, exponent=None)
                else:
                    annotation=''
            
            x1 = periods_maxpeaks[j]*1.3
            y1 = peakvalues_plot[j] #- deltaY/10
            if np.log10(np.abs(x1/maxperiod))>0.85:
                x1 = periods_maxpeaks[j]*0.8
            #if np.log10((x1 - minperiod)/minperiod)<0.1
            
            #deltalogp = np.lod10(max(periods) - min(periods))
            diff_y = np.abs(y1 - y_legend[:j])
            diff_x = np.abs((np.log10(x1/x_legend[:j])))
            
            condition = (diff_y <deltaY/9) *  (diff_x<deltaX/9)
            index_cond = [i for i,v in enumerate(condition) if v]
            
    
            indices = np.arange(j)
            if j>0 and np.sum(condition)>0:
                distx = diff_x[index_cond]
                ii = indices[condition][np.argmin(distx)]
                if y1 <y_legend[ii]:
                    if y1>deltaY/10:
                        y1 = y_legend[ii] - deltaY/10
                    else:
                        x1 = x1* 1.1
                else:
                    y1 = y_legend[ii] + deltaY/10
            y_legend[j] = y1 
            x_legend[j] = x1                 
            
            if annotation is not None:
                ax1.annotate(annotation, (x1,y1),
                             ha='left', fontsize=16, 
                             color=(0.85,0.325,0.098),
                             bbox=dict(facecolor='white', 
                                       edgecolor = 'white',
                                       alpha=0.8))         
        
        ax1.tick_params(axis='y', colors=colorfip)
        #ax2.tick_params(axis='y', colors=colortip)
        ax1.set_xlim([self.periods[0], self.periods[-1]])
        #ax2.set_ylim([-8, 0 ])     
        ax1.set_xlabel('Period (days)', fontsize=18)     
        plt.suptitle('FIP periodogram',fontsize=20,y=0.97)
        ax1.legend(fontsize = 16, loc='best')
        fig.suptitle(fipperio_title ,fontsize=20,y=0.97)    
        
        if save:
            string_save = self.starname.replace(' ', '_') + '_FIP_periodogram_notext.pdf'
            plt.savefig(string_save , rasterized = True,
                        format='pdf')
            
            
            
    def plot_alpha(self, save=True, 
                   suffix = '',zoom_factor=4):
            
        x = self.fiplevel
        ys = self.truepos
        errs = self.bernouilli_unc
        nsim = ys.shape[0]

        diffs = ys.copy()
        for i in range(nsim):
            diffs[i,:] = ys[i,:] - x
        
        maxdif = np.max(diffs)
        mindif = np.min(diffs)
        ratio = (maxdif-mindif)*zoom_factor
        

        fig, (ax1, ax2) = plt.subplots(2, 1, 
             figsize=(6,6),sharex=True,gridspec_kw={
                           'height_ratios': [1,ratio]})        
#        fig = plt.figure(figsize=(6,7))
#        spec = gridspec.GridSpec(ncols=1, nrows=2,
#                         height_ratios=[2, 1])
#        ax1 = fig.add_subplot(spec[0])
#        ax2 = fig.add_subplot(spec[1], sharex = ax1)
        
        #ax1.set_aspect('equal')
        #ax2.set_aspect('equal')
        ax1.set_xlim(-0.05,1.05)
        #ax1.set_ylim(-0.05,1.05)
        

        #plt.subplots(1, 2, figsize=(10, 4.2))
      
        ax2.set_xlabel('True inclusion probability (TIP)' 
                   ,fontsize=16)
        #ax2.set_xlabel('True inclusion probability (TIP)' 
        #           ,fontsize=16)      
        #ax1.set_aspect('equal')
        
        ax1.set_ylabel('Fraction of success', fontsize=16) 
#        ax2.yaxis.set_label_position("right")
#        ax2.yaxis.tick_right()
        
        ax2.set_ylabel('Fration of\nsuccess normalized', fontsize=16) 
        ax1.tick_params(axis='both', which='major', labelsize=14)
        ax2.tick_params(axis='both', which='major', labelsize=14)
        fig.suptitle('Fraction of success vs. TIP',fontsize=18)
        
        ax1.plot([0,1], [0,1], linestyle ='--',color='black', 
                 label = 'y = x')
        ax2.plot([0,1], [0,0], linestyle ='--',color='black')
        
        for i in range(nsim):
            ax1.errorbar(x, ys[i,:],errs[i,:],
                             fmt='o',alpha=0.7)
            diff = ys[i,:] - x
            ax2.errorbar(x, diff, errs[i,:],fmt='o',alpha=0.7)
        ax1.legend(fontsize=14)
            
        plt.gcf().subplots_adjust(left=0.23)
        if save:
            plt.savefig('alphacheck_' +suffix+ '.pdf', fmt='pdf')

#import fip_plots
#c = fip_plots.fip_plots()
#c.fiplevel = np.array([0, .2, .4, .6,.8,.9,.95,.99])
#mm = np.zeros((5,8))
#for i in range(5):
#    mm[i,:] = c.fiplevel + np.random.randn(8)*.1
#c.truepos = mm
#c.bernouilli_unc = np.ones((5,8))*.1
#c.plot_alpha(suffix='test')


def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """
    written by sodd (stackoverflow user)
    
    Returns a string representation of the scientific
    notation of the given number formatted for use with
    LaTeX or Mathtext, with specified number of significant
    decimal digits and precision (number of decimal digits
    to show). The exponent to be used can also be specified
    explicitly.
    """
    if num!=0 and ~np.isnan(num):
        if exponent is None:
            exponent = int(np.floor(np.log10(abs(num))))
        coeff = round(num / float(10**exponent), decimal_digits)
        if precision is None:
            precision = decimal_digits
        if exponent !=0:
            return r"${0:.{2}f}\cdot10^{{{1:d}}}$".format(coeff, exponent, precision)
        else:
            return r"${0:.{2}f}$".format(coeff, exponent, precision)
    else:
        return('0')   