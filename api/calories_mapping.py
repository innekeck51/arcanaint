import pandas as pd


class CaloriesMapping():
    def get_long_lat(self, file, level_calories):
        data = pd.read_excel(file, engine='openpyxl')
        new = pd.DataFrame(self.filter_by_calories(data, level_calories))
        new[["AreaName", "BoreholeName", "Calories", "From", "To"]]

        new.loc[new['BoreholeName'] == "MJ01", 'Longitude'] = -2.929919
        new.loc[new['BoreholeName'] == "MJ01", 'Latitude'] = 103.55111

        new.loc[new['BoreholeName'] == "MJ02", 'Longitude'] = -2.942281
        new.loc[new['BoreholeName'] == "MJ02", 'Latitude'] = 103.62083

        new.loc[new['BoreholeName'] == "LD01", 'Longitude'] = -3.00187
        new.loc[new['BoreholeName'] == "LD01", 'Latitude'] = 103.667924

        new.loc[new['BoreholeName'] == "LD02", 'Longitude'] = -2.9906551
        new.loc[new['BoreholeName'] == "LD02", 'Latitude'] = 103.68307

        new.loc[new['BoreholeName'] == "LD03", 'Longitude'] = -2.975489
        new.loc[new['BoreholeName'] == "LD03", 'Latitude'] = 103.625422

        new.loc[new['BoreholeName'] == "LD04", 'Longitude'] = -2.95997
        new.loc[new['BoreholeName'] == "LD04", 'Latitude'] = 103.656423

        new.loc[new['BoreholeName'] == "LD05", 'Longitude'] = -2.963333
        new.loc[new['BoreholeName'] == "LD05", 'Latitude'] = 103.618663

        new.loc[new['BoreholeName'] == "LD06", 'Longitude'] = -2.932254
        new.loc[new['BoreholeName'] == "LD06", 'Latitude'] = 103.609165

        new.loc[new['BoreholeName'] == "LD07", 'Longitude'] = -2.97098
        new.loc[new['BoreholeName'] == "LD07", 'Latitude'] = 103.551822

        new.loc[new['BoreholeName'] == "LD08", 'Longitude'] = -2.940444
        new.loc[new['BoreholeName'] == "LD08", 'Latitude'] = 103.528968

        new.loc[new['BoreholeName'] == "LD09", 'Longitude'] = -2.959055
        new.loc[new['BoreholeName'] == "LD09", 'Latitude'] = 103.561634

        new.loc[new['BoreholeName'] == "LD10", 'Longitude'] = -2.911795
        new.loc[new['BoreholeName'] == "LD10", 'Latitude'] = 103.623476

        new.loc[new['BoreholeName'] == "LD11", 'Longitude'] = -2.862449
        new.loc[new['BoreholeName'] == "LD11", 'Latitude'] = 103.587203

        new.loc[new['BoreholeName'] == "LD12", 'Longitude'] = -2.86429
        new.loc[new['BoreholeName'] == "LD12", 'Latitude'] = 103.583396

        subset = new[["Longitude", "Latitude"]]
        tuples = [tuple(x) for x in subset.to_numpy()]
        return tuples

    def filter_by_calories(self, data, category):
        if(category == "low"):
            return data[data["Calories"] < 5100]
        if(category == "medium"):
            return data[(data["Calories"] >= 5100) & (data["Calories"] < 6100)]
        if(category == "high"):
            return data[(data["Calories"] >= 6100) & (data["Calories"] < 7100)]
        if(category == "very high"):
            return data[data["Calories"] > 7100]
        else:
            return data
