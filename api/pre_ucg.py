import pandas as pd
import matplotlib.pyplot as plt


class PreUCG():
    def calculateUCG(self, file, boreholeName):
        df = pd.read_csv(file)
        data2 = df
        # Menghitung Depth to Thickness Ratio
        df['D/T Ratio'] = df['From'] / df['Thickness']

        def f(row):
            if (row['D/T Ratio'] >= 120) and (row['D/T Ratio'] < 200):
                val = '22'
            elif (row['D/T Ratio'] >= 200) and (row['D/T Ratio'] < 300):
                val = '18'
            elif (row['D/T Ratio'] >= 300) and (row['D/T Ratio'] < 400):
                val = '15'
            elif row['D/T Ratio'] > 400:
                val = '15'
            else:
                val = 'Tidak Memenuhi Kriteria'
            return val

        df['Rasio'] = df.apply(f, axis=1)

        data2 = data2.loc[df['Borehole Name'] == boreholeName]
        df2 = pd.DataFrame(data2)

        # membuat kolom baru untuk Roof dan Floor
        df2['Roof'] = df2.apply(lambda _: '', axis=1)
        df2['Floor'] = df2.apply(lambda _: '', axis=1)

        for index, row in df2.iterrows():
            if row['Lithology'] == "Coal":
                df2.loc[index, 'Roof'] = df2.loc[(index - 1), 'Lithology']
                df2.loc[index, 'Floor'] = df2.loc[(index + 1), 'Lithology']

        # membuat kolom baru untuk Roof dan Floor
        df2['Roof Thickness'] = df2.apply(lambda _: '', axis=1)
        df2['Floor Thickness'] = df2.apply(lambda _: '', axis=1)
        df2['Roof/Floor Ratio'] = df2.apply(lambda _: '', axis=1)

        for index, row in df2.iterrows():
            if row['Lithology'] == "Coal":

                # Counting Floor Thickness
                if("sandstone" in df2.loc[(index - 1), 'Lithology'].lower()):
                    df2.loc[index, 'Roof Thickness'] = df2.loc[(
                        index - 1), 'Thickness']
                else:
                    indexRoof = 1
                    while("sandstone" not in df2.loc[(index - indexRoof), 'Lithology'].lower()):
                        if(((index - indexRoof) < df2.shape[0]) & ((index - indexRoof) > 0)):
                            indexRoof = indexRoof+1
                        else:
                            break

                    resultRoof = 0
                    for x in range(1, indexRoof+1):
                        if((df2.loc[(index - x), 'Lithology'] != "Coal") & ("sandstone" not in df2.loc[(index - x), 'Lithology'].lower())):
                            resultRoof += df2.loc[(index - x), 'Thickness']
                            df2.loc[index, 'Roof Thickness'] = resultRoof
                        else:
                            break

        for index, row in df2.iterrows():
            if row['Lithology'] == "Coal":

                # Counting Floor Thickness
                if("sandstone" in df2.loc[(index + 1), 'Lithology'].lower()):
                    df2.loc[index, 'Floor Thickness'] = df2.loc[(
                        index + 1), 'Thickness']
                else:
                    indexFloor = 1
                    while(("sandstone" not in df2.loc[(index + indexFloor), 'Lithology'].lower())):
                        if(((index + indexFloor) < (df2.shape[0]-1)) & ((index + indexFloor) > 0)):
                            indexFloor = indexFloor+1
                        else:
                            break

                    resultFloor = 0
                    for x in range(1, indexFloor+1):
                        if((df2.loc[(index + x), 'Lithology'] != "Coal") & ("sandstone" not in df2.loc[(index + x), 'Lithology'].lower())):
                            resultFloor += df2.loc[(index + x), 'Thickness']
                            df2.loc[index, 'Floor Thickness'] = resultFloor
                        else:
                            break

        return df2.drop(["Roof", "Floor"], axis=1).to_json(orient='table')
