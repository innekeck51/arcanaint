import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt


class ASTM():
    def calculateLSTM(self, file, boreholeName, tipe):
        data = pd.read_csv(file)
        df = pd.DataFrame(data)
        # penjumlahan M dan A adalah MA
        df['MA'] = df['M (%)'] + df['A (%)']
        df['Conversion Factor'] = 100 / (100 - df['MA'])
        df['CV (daf)'] = df['CV(adb)'] * df['Conversion Factor']
        df['Net CV (Btu/lb)'] = df['CV (daf)'] - \
            (91.2 * df['H (%)']) - (10.5 * df['M (%)'])
        df['Atom C'] = df['C (%)']/12
        df['Atom O'] = df['O (%)']/16
        df['Atom H'] = df['H (%)']/1
        df['O/C'] = df['Atom O'] / df['Atom C']
        df['H/C'] = df['Atom H'] / df['Atom C']

        def mappingCalories(row):
            if row['CV(adb)'] < 5100:
                val = 'Low'
            elif (row['CV(adb)'] >= 5100) and (row['CV(adb)'] < 6100):
                val = 'Medium'
            elif (row['CV(adb)'] >= 6100) and (row['CV(adb)'] < 7100):
                val = 'High'
            elif row['CV(adb)'] > 7100:
                val = 'Very High'
            else:
                val = 'NaN'
            return val

        df['Calorific Value'] = df.apply(mappingCalories, axis=1)

        def calculatingASTM(row):
            if row['Net CV (Btu/lb)'] < 6300:
                val = 'Lignite B'
            elif (row['Net CV (Btu/lb)'] >= 6300) and (row['Net CV (Btu/lb)'] < 8300):
                val = 'Lignite A'
            elif (row['Net CV (Btu/lb)'] >= 8300) and (row['Net CV (Btu/lb)'] < 9500):
                val = 'Subbituminous C'
            elif (row['Net CV (Btu/lb)'] >= 9500) and (row['Net CV (Btu/lb)'] < 10500):
                val = 'Subbituminous B'
            elif (row['Net CV (Btu/lb)'] >= 10500) and (row['Net CV (Btu/lb)'] < 11500):
                val = 'Subbituminous A'
            elif (row['Net CV (Btu/lb)'] >= 11500) and (row['Net CV (Btu/lb)'] < 13000):
                val = 'Bituminous High Vol C'
            elif (row['Net CV (Btu/lb)'] >= 13000) and (row['Net CV (Btu/lb)'] < 14000):
                val = 'Bituminous High Vol B'
            elif row['Net CV (Btu/lb)'] > 14000:
                val = 'Bituminous High Vol A'
            else:
                val = 'NaN'
            return val

        df['ASTM'] = df.apply(calculatingASTM, axis=1)

        # cara 1: pisahin per borehole
        gb = df.groupby('Borehole')
        [gb.get_group(x) for x in gb.groups]

        # Bisa cara 2, dan ini bisa berulang, mudah diaplikasikan untuk scatterplotnya
        for z in gb.groups:
            keep = gb.get_group(z)

        buf = BytesIO()
        # ASTM analysis per borehole
        # Atomic Ratio per Borehole
        if(tipe == "ASTM"):
            for z in gb.groups:
                if(z == boreholeName):
                    keep = gb.get_group(z)
                    y1 = keep['Net CV (Btu/lb)']
                    x1 = keep['ASTM']
                    #colors={'Lignite A':'red','Lignite B':'blue','Subbituminous B':'green'}
                    #color_ls=[colors[i] for i in x]
                    plt.figure(figsize=(10, 10))
                    plt.title(f'ASTM Analysis-{z}')
                    plt.xlabel('Coal Rank')
                    plt.ylabel('Net CV (Btu/lb)')
                    plt.scatter(x1, y1, marker='*', s=20, alpha=1)
                    fig2 = plt.gcf()
                    plt.draw()
                    fig2.savefig(buf, transparent='True',
                                 dpi=300, format='svg')

        # CV analysis per borehole
        if(tipe == "Calorific"):
            for z in gb.groups:
                if(z == boreholeName):
                    keep = gb.get_group(z)
                    y = keep['CV(adb)']
                    x = keep['Calorific Value']
                    # colors={'LOW':'red','MEDIUM':'blue','HIGH':'green'}
                    #color_ls=[colors[i] for i in x]
                    plt.title(f'Calorific Value Analysis-{z}')
                    plt.xlabel('Coal Rank')
                    plt.ylabel('CV (adb) (kcal/kg)')
                    plt.scatter(x, y, marker='*', s=40, alpha=1)
                    fig1 = plt.gcf()
                    plt.show()
                    plt.draw()
                    fig1.savefig(buf, transparent='True',
                                 dpi=300, format='svg')

        return buf
