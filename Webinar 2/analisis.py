#!/usr/bin/env python
# -*- coding: utf-8 -*-


## UTILIDADES

def ajustado(df):
    df=df.copy()
    lista=['Open','High','Low']   
    for f in lista:
        df[f]=df[f]*df['Adj Close']/df['Close']
    df=df.drop('Close', axis=1)
    df=df.rename(columns = {'Adj Close': 'Close'} )
    return df

def rolling_window(a, window, step=1):
    '''
    Rolling window of a numpy array.
    --------
    a : Numpy array
    window : number of elements in window 
    step : step to take elements for window
    '''
    shape = a.shape[:-1] + (a.shape[-1] - step *(window -1) , window)
    strides = a.strides + (a.strides[-1]*step,)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)



## ANALIZADORES



def sharpe_anual(retornos_trades, N=252):
    import numpy as np
    return np.sqrt(N) * retornos_trades.mean() / retornos_trades.std()


def SQN (rets, n_rets=None):
    import numpy as np
    ret_medio = rets.stack().mean()
    ret_std = rets.stack().std()
    if n_rets == None :
        try:
            n_rets = len (rets)
        except:
            n_rets = rets.shape[0]
    sqn = np.sqrt(n_rets) * ret_medio / ret_std
    return sqn


def DrawDown (rets, info=True):
    import numpy as np
    # rets es una serie de Pandas con los retornos
    rets = rets.fillna(0).add(1).cumprod()
    dd = rets.div(rets.cummax()).sub(1)
    maxdd = dd.min()
    fmaxdd = dd.idxmin()
    inicio = rets.loc[:fmaxdd].idxmax()
    try:
        fin = dd[fmaxdd:][dd[fmaxdd:]==0].index[0]
    except:
        fin = np.nan    
    if info:
        if fin != fin:
            print ('Máximo Drawdown : {}% \nInicio : {} \nAún en curso'.format(-round(maxdd*100,2), inicio.date() ))
        else:
            print ('Máximo Drawdown : {}% \nInicio : {} \nFin    : {}'.format(-round(maxdd*100,2), inicio.date(), fin.date() ))
    return dd, maxdd, inicio, fin


def beneficio_neto(retornos):

    retorno_acumulado = retornos.add(1).cumprod()
    benefio = retorno_acumulado[-1] - retorno_acumulado[0]
    return benefio



def recovery_factor(retornos):

    # Debe pasarse los retornos en base 1

    benef_neto = beneficio_neto(retornos.fillna(0))
    dd, maxdd, inicio, fin = DrawDown(retornos, info=False)
    rf = -(benef_neto/ maxdd)
    return rf




def CAGR(retornos):
    '''
        Devuelve la Tasa de crecimiento anual compuesto - CAGR.
        ----

        retornos :  Pandas Serie con los retornos, el indice debe ser datetime

        ----
    '''
    retorno_acumulado = retornos.fillna(0).add(1).cumprod()
    cagr = (retorno_acumulado[-1] / retorno_acumulado[0]) ** (
                365 / (retornos.index[-1] - retornos.index[0]).days ) - 1
    return cagr


def profit_factor(trades):

    trades = trades.fillna(0)
    trades = trades[trades > 0].sum().sum()
    ret_neg = trades[trades < 0].sum().sum()
    profit_factor = ret_pos / -ret_neg
    return profit_factor


def rentabilidad_mensual (rets):

    '''


    :param rets: Pandas serie of returns with a datetime index.
    :return: A pivot table with % return by years and months
    '''
    rs = pd.DataFrame((rets.copy()*100), columns=['Rentabilidad %'])
    rs2 = rs.resample('M').sum().copy()
    # rs2['Rentabilidad'] = rs['Rentabilidad']*100
    rs2['Año']=rs2.index.year
    rs2['Mes']=rs2.index.month
    pv = rs2.pivot(index='Año', columns='Mes').fillna(0).style.bar(align='mid', color=['#d65f5f', '#5fba7d']).format('{:.2f}')
    return pv


## VISUALIZACIONES

def donut (porcentaje, titulo, color='green'):
    from matplotlib import pyplot as plt


    fig = plt.figure(figsize=(6, 6))
    fig.patch.set_facecolor('white')

    plt.rcParams['text.color'] = color

    plt.title(titulo, fontsize=40)
    my_circle = plt.Circle((0, 0), 0.75, color='white')

    # Pieplot + circle on it
    giro = min(porcentaje,1)
    plt.pie([giro, 1 - giro], colors=[color, '0.95'])

    p = plt.gcf()
    p.gca().add_artist(my_circle)

    l = len(str(porcentaje))

    plt.text(0 - 0.05 * l, -0.05, f"{round(porcentaje*100,2)}%", fontsize=40)

    plt.show()

    return




# Tridimensional
def trisurf_heatmap (df, dim1, dim2, dim3, v1=45, v2=15):
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_trisurf(df[dim1], df[dim2], df[dim3], cmap=plt.cm.jet, linewidth=0.1, alpha = 0.8)

    fig.colorbar( surf, shrink=0.5, aspect=5)
    ax.view_init(v1, v2)

    plt.show()
    return
