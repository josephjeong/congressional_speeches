import pandas as pd

df = pd.read_csv("temp/speeches.csv", sep="|")
print(df.shape)

# df = pd.read_parquet("temp/corpus.gzip", engine="pyarrow")
# print(df[(df["l_name"] == "TIPTON") & (df["speech_id"] < 150000)])

df = pd.read_csv("temp\speakermap.csv", sep="|")
print(df)
df.drop_duplicates(subset=["speech"], inplace=True)
# df = df[df.duplicated(subset=["speech"], keep=False)]
print(df)

df = pd.read_csv("temp\speakermap_duplicates.csv", sep="|")
print(df)
df.dropna(inplace=True)
df.drop_duplicates(subset=["speech"], inplace=True)
print(df)

# df.sort_values(by=["speech"]).head(5000).to_csv("check/bruh.csv", sep="|")



# print(df.shape[0])

# df.dropna(subset=["bioname"], inplace=True)

# print(df.shape[0])

# df_dupe = df[df.duplicated(subset=["house", "month", "day", "year", "speech", "l_name", "datetime"], keep=False)]
# df.drop_duplicates(subset=["house", "month", "day", "year", "speech", "l_name", "datetime"], inplace=True)

# df_rows = df.shape[0]
# df_dupe_rows = df_dupe.shape[0]

# print(df_rows, df_dupe_rows, df_rows + df_dupe_rows)

# print(df_dupe.sort_values(by=["speech"]).head(100))
# print(df.sort_values(by=["speech"]).head(100))
"""
Some of them seem to have only a NaN duplicate. THis is not intended behaviour.
Before Dropna:
                            house    month  day  year    clean_names                                             speech  l_name gender  ...                 bioname state  party_name congress district  chamber  Begin Date Adjourn Date
477218   HOUSE OF REPRESENTATIVES  January   21  1863          TRAIN      ♀  THE CONGRESSIONAL GLOBE.    January 28,      TRAIN      M  ...  TRAIN, Charles Russell    MA  Republican     37.0      8.0    House  1861-03-04   1863-03-03
1479298  HOUSE OF REPRESENTATIVES  January   21  1863          TRAIN      ♀  THE CONGRESSIONAL GLOBE.    January 28,      TRAIN      M  ...                     NaN   NaN         NaN      NaN      NaN      NaN         NaN          NaN
390075   HOUSE OF REPRESENTATIVES    april   11  1860           HILL                     ♀  TUE CONGRESSIONAL GLOBE.       HILL      M  ...            HILL, Joshua    GA  Opposition     36.0      7.0    House  1859-03-04   1861-03-03
1387980  HOUSE OF REPRESENTATIVES    april   11  1860           HILL                     ♀  TUE CONGRESSIONAL GLOBE.       HILL      M  ...                     NaN   NaN         NaN      NaN      NaN      NaN         NaN          NaN
1047151  HOUSE OF REPRESENTATIVES    March   19  1838         SNYDER                                     lion of the...  SNYDER      M  ...                     NaN   NaN         NaN      NaN      NaN      NaN         NaN          NaN
...                           ...      ...  ...   ...            ...                                                ...     ...    ...  ...                     ...   ...         ...      ...      ...      ...         ...          ...
53837    HOUSE OF REPRESENTATIVES   August   13  1842  CHARLES BROWN               made a similar in  quiry.  The CH...   BROWN      M  ...           BROWN, Milton    TN        Whig     27.0     12.0    House  1841-03-04   1843-03-03
1081896  HOUSE OF REPRESENTATIVES   August   13  1842  CHARLES BROWN               made a similar in  quiry.  The CH...   BROWN      M  ...                     NaN   NaN         NaN      NaN      NaN      NaN         NaN          NaN
53838    HOUSE OF REPRESENTATIVES   August   13  1842  CHARLES BROWN               made a similar in  quiry.  The CH...   BROWN      M  ...          BROWN, Charles    PA    Democrat     27.0      1.0    House  1841-03-04   1843-03-03
53839    HOUSE OF REPRESENTATIVES   August   13  1842  CHARLES BROWN               made a similar in  quiry.  The CH...   BROWN      M  ...    BROWN, Aaron Venable    TN    Democrat     27.0     10.0    House  1841-03-04   1843-03-03
53836    HOUSE OF REPRESENTATIVES   August   13  1842  CHARLES BROWN               made a similar in  quiry.  The CH...   BROWN      M  ...         BROWN, Jeremiah    PA        Whig     27.0      4.0    House  1841-03-04   1843-03-03

After Dropna:
                           house     month  day  year clean_names                                             speech      l_name gender  ...                         bioname state  party_name congress district  chamber  Begin Date Adjourn Date
477218  HOUSE OF REPRESENTATIVES   January   21  1863       TRAIN      ♀  THE CONGRESSIONAL GLOBE.    January 28,          TRAIN      M  ...          TRAIN, Charles Russell    MA  Republican     37.0      8.0    House  1861-03-04   1863-03-03
390075  HOUSE OF REPRESENTATIVES     april   11  1860        HILL                     ♀  TUE CONGRESSIONAL GLOBE.           HILL      M  ...                    HILL, Joshua    GA  Opposition     36.0      7.0    House  1859-03-04   1861-03-03
19612   HOUSE OF REPRESENTATIVES     March   19  1838      SNYDER                                     lion of the...      SNYDER      M  ...             SNYDER, Adam Wilson    IL    Democrat     25.0      1.0    House  1837-03-04   1839-03-03
19610   HOUSE OF REPRESENTATIVES     March   19  1838     GARLAND                                    adjustment o...     GARLAND      M  ...                   GARLAND, Rice    LA        Whig     25.0      3.0    House  1837-03-04   1839-03-03
19611   HOUSE OF REPRESENTATIVES     March   19  1838     GARLAND                                    adjustment o...     GARLAND      M  ...                  GARLAND, James    VA    Democrat     25.0     12.0    House  1837-03-04   1839-03-03
...                          ...       ...  ...   ...         ...                                                ...         ...    ...  ...                             ...   ...         ...      ...      ...      ...         ...          ...
262548  HOUSE OF REPRESENTATIVES   January   15  1856   GREENWOOD             I give notice to the  House that I ...   GREENWOOD      M  ...        GREENWOOD, Alfred Burton    AR    Democrat     34.0      1.0    House  1855-12-03   1857-03-03
506211  HOUSE OF REPRESENTATIVES     April   25  1864   PENDLETON             I have a number of  amendments to o...   PENDLETON      M  ...          PENDLETON, George Hunt    OH    Democrat     38.0      1.0    House  1863-03-04   1865-03-03
403337  HOUSE OF REPRESENTATIVES      June    5  1860    CRAWFORD             I have no objection to  having the ...    CRAWFORD      M  ...        CRAWFORD, Martin Jenkins    GA    Democrat     36.0      2.0    House  1859-03-04   1861-03-03
174855  HOUSE OF REPRESENTATIVES      July   28  1852  CHURCHWELL             I hope the amend  nent will pass. M...  CHURCHWELL      M  ...  CHURCHWELL, William Montgomery    TN    Democrat     32.0      3.0    House  1851-03-04   1853-03-03
297803  HOUSE OF REPRESENTATIVES  February   21  1857    FLORENCE             I move the followin  amendment, to ...    FLORENCE      M  ...          FLORENCE, Thomas Birch    PA    Democrat     34.0      1.0    House  1855-12-03   1857-03-03

[100 rows x 18 columns]
"""