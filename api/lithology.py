import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


class Lithology():
    def lithology_classification(self, file, boreholeName, dictionaryLitho):
        data_lithology = pd.read_csv(file)
        gb = data_lithology.groupby('Borehole Name')
        [gb.get_group(x) for x in gb.groups]

        for z in gb.groups:
            keep = gb.get_group(z)

        lithology_numbers = dictionaryLitho
        df_lith = pd.DataFrame.from_dict(lithology_numbers, orient='index')
        df_lith.index.name = 'LITHOLOGY'
        result = data_lithology.replace(
            dict(zip(df_lith.lith, df_lith.index)))
        keep = pd.DataFrame(result)
        test = keep[keep["Borehole Name"] ==
                    boreholeName].reset_index(drop=True)
        test = test[::-1]
        return self.makeplot(test, lithology_numbers)

    def makeplot(self, well, lithology_numbers):
        fig, ax = plt.subplots(figsize=(50, 20))

        # Set up the plot axes
        ax4 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)

        # Lithology track
        ax4.plot(well['To'], color="black", linewidth=0.5)
        ax4.set_xlabel("Lithology")
        ax4.set_xlim(0, 1)
        ax4.xaxis.label.set_color("black")
        ax4.tick_params(axis='x', colors="black")
        ax4.spines["top"].set_edgecolor("black")

        for x in range(well.shape[0]):
            key = well['Lithology'][x]
            selectColor = lithology_numbers[key]['color']
            hatch = lithology_numbers[key]['hatch']
            ax4.fill_betweenx(y=[well['From'][x], well["To"][x]],
                              x1=0, x2=2, facecolor=selectColor, hatch=hatch)

        plt.tight_layout()
        yticks = np.arange(well["From"].min(), well["To"].max()+10, 10)
        plt.yticks(yticks)
        plt.gca().invert_yaxis()
        fig.subplots_adjust(wspace=0.15)
        buf = BytesIO()
        plt.savefig(buf, bbox_inches='tight', format='png')
        return buf
