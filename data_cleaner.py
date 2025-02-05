import pandas as pd
import re
 
df1 = pd.read_csv('datasets/taylor-swift-songs.csv', index_col=0)
df2 = pd.read_csv('datasets/taylor-swift-tracks.csv', index_col=0)

df1 = df1.dropna()
df1 = df1.loc[df1['url'].str.contains('lyrics')]
df1.sort_values(by=['album'], inplace=True)

dfg = df1.copy()
dfs = df2.copy()

for df in (dfg, dfs):
    
    df['title'] = df['title'].str.strip()
    df['title'] = df['title'].str.lower()
    df['title'] = df['title'].str.replace(r'[^a-zA-Z0-9]', '')

merged = pd.merge(dfs, dfg, on=['title'], how='inner')

for i, r in merged.iterrows():
    for j, m in df2.iterrows():

        title = m['title'].strip().lower()
        title = re.sub('[^a-zA-Z0-9]', '', title)
        
        if r['title'] == title:
            merged.iloc[i, df.columns.get_loc('title')] = m['title']

merged = merged.drop(['album_y'], axis=1)
merged = merged.rename(columns={'album_x':'album'})
merged.to_csv('datasets/songs-with-urls.csv')