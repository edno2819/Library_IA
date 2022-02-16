from utilsIA import *
import pandas as pd

df = pd.read_excel('BASE_NLP.xlsx', header=[0])
df.head()
ProcessingData.showLabelsQtd(df, 'CLASSIFICAÇÃO')
df = ProcessingData.applyFunction(df, 'CLASSIFICAÇÃO', lambda x: x.upper())
ProcessingData.showLabelsQtd(df, 'CLASSIFICAÇÃO')
GraphDatas.labelsData(df['CLASSIFICAÇÃO'])
df_encoder = ProcessingData.encoderDf(df, 'CLASSIFICAÇÃO')
df['LABELS'] = df_encoder.transform(df['CLASSIFICAÇÃO'].values)
df_balanced = ProcessingData.balancedData(df, 'LABELS', 91)
df