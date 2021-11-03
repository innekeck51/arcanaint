import pandas as pd


class UCG():
    def calculateUCG(self, file):
        data = pd.read_csv(file)
        a = data[data["CV(adb)"] < 6100]
        b = a[(a['ASTM'].str.startswith('Lignite')) & (a['Thickness'] > 3.5)]
        c = a[(~a['ASTM'].str.startswith('Lignite', na=False))
              & (a['Thickness'] > 2.0)]
        data_new = pd.concat([c, b])
        d = data_new.loc[(data_new['From'].between(120, 200))
                         & (data_new['D/T Ratio'] >= 22)]
        e = data_new.loc[(data_new['From'].between(200, 300))
                         & (data_new['D/T Ratio'] >= 18)]
        f = data_new.loc[(data_new['From'].between(300, 400))
                         & (data_new['D/T Ratio'] >= 15)]
        g = data_new.loc[(data_new['From'] > 400) &
                         (data_new['D/T Ratio'] >= 15)]
        data_step3 = pd.concat([d, e, f, g])
        keep = {'Roof': ['Siltstone', 'Claystone', 'Carbonaceous Claystone', 'Tuff', 'Alternation Sandstone - Mudstone', 'Shale', 'Coaly Shale', 'Core Loss'],
                'Floor': ['Siltstone', 'Claystone', 'Carbonaceous Claystone', 'Tuff', 'Alternation Sandstone - Mudstone', 'Shale', 'Coaly Shale', 'Core Loss']}
        h = data_step3[data_step3[list(keep)].isin(keep).all(axis=1)]
        result = h
        return result.to_json(orient='table')
