
import pandas as pd
import numpy as np


dates=pd.date_range('20180820',periods=6)
s=pd.Series([1,2,5,np.nan,8,9],index=dates)
df=pd.DataFrame(np.random.randn(6,4),columns=list('ABCD'))
df['F']=df['A']+df['B']
del df['A']
#print(df['B'].cov(df['D']))
print(df.rolling(window=3).mean())
print(df.expanding(min_periods=3).mean())
# def adder(ele1,ele2):
#     return ele1+ele2
# df1=df.pipe(adder,2)
# print(df1)

