# imports, i guess?
import pandas as pd
import numpy as np

def importMulticomponent(fn, sheet_name="Multicomponent Data", dropNA=True):
    '''Wrapper to import the excel file of StepOnePlus multicomponent data'''
    data = pd.read_excel(fn, skiprows=range(0, 7), sheet_name=sheet_name)
    if dropNA:
        data = data.dropna(axis=1,
                           how="all")  #import + drop any weird empty columns
    return data  #import just the data

## FN: import amplification
def importAmplification(fn, sheet_name="Amplification Data", dropNA=True):
    '''Wrapper to import the excel file of StepOnePlus amplification data'''
    data = pd.read_excel(fn, skiprows=range(0, 7), sheet_name=sheet_name)
    if dropNA:
        data = data.dropna(how="any")  #import + drop any weird empty columns
    return data  #import just the data

#FN to plot cycles, takes directly from data from importMulticomponent + returns set of axes
def plotMulti(data):
    '''helper to plot cycle fluoresence from importMultiComponent'''
    data = data.drop(
        columns=['Dye', 'CycleStart', 'netChange']).dropna().rename(
            columns=lambda x: x.lstrip("Cycle ").zfill(2))
    melted = data.melt(id_vars="Well")
    ax = sns.lineplot(x='variable', y='value', hue='Well', data=melted, loc = "best")
    ax.set(xlabel='Cycle', ylabel='Sybr Green')
    return ax


def plotAmp(melted):
    '''helper to plot cycle fluoresence from importMultiComponent'''
#     melted = df.drop(columns = 'netChange').melt(id_vars = 'Well')
    melted['_well'] = '_' + melted['Well']
    ax = sns.lineplot(x='Cycle', y='ΔRn', hue='_well', data=melted)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    return ax

def importWrapper(fn, target=None):
    outputfn = fn.rstrip('.xls')
    melted = importAmplification(fn, dropNA=True).reset_index(drop=True)
    if target:
        melted = melted[melted['Target Name'].str.contains(target)]
        target = "- {} -".format(target)
    cycleCT = melted.Cycle.max()
    title = "{} {} {} cycles".format(outputfn, target, str(cycleCT))
    df = melted.pivot(index='Well', columns='Cycle',
                      values='ΔRn').dropna().reset_index()
    vals = df[cycleCT]
    return outputfn, melted, cycleCT, title, df, vals
