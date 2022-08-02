from dash import Dash, html, dcc
import plotly.express as px
import re
import pandas as pd
import numpy as np

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv("data/OccupancySummaryJuly22.csv")
df.drop('vacant', axis=1)
df.drop('unit_type', axis=1)
occ_df = df[[ 'size', 'total_units', 'occupied', 'occupied_percentage', 'rent', 'p_std_gross_revenue']]

occ_df['isCompany'] = np.where(df['unit_type'] == 'Company Unit', 1, 0)
occ_df['isExterior'] = np.where(df['unit_type'] == 'Exterior Unit', 1, 0)
occ_df['isGround'] = np.where(df['unit_type'] == 'Ground Unit', 1, 0)
occ_df['isLocker'] = np.where(df['unit_type'] == 'Locker', 1, 0)
occ_df['hasClimateControl'] = np.where(df['unit_type'] == 'Non-Climate Interior', 0, 1)
occ_df['isRollup'] = np.where(df['unit_type'] == "Roll Up's", 1, 0)
occ_df['isStorage'] = np.where(df['unit_type'] == 'Storage Unit', 1, 0)

def splitSize(sizes):
    length = []
    width = []
    price = []
    for size in sizes:
        arr = size.split('-')
        sizesArr = re.findall("[0-9]+", arr[0])
        length.append(sizesArr[0])
        width.append(sizesArr[1])
        price.append(arr[1])
    return length, width, price

length, width, price = splitSize(occ_df['size'])
occ_df.insert(0, 'length', length)
occ_df.insert(1, 'width', width)
occ_df.insert(2, 'price', price)
occ = occ_df.drop('size', axis=1)


def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )

app.layout = html.Div([
    html.H1('Occupancy Summary June 2022'),
    html.H2('Ballpark Storage Facility'),
    generate_table(occ)
])

if __name__ == '__main__':
    app.run_server(debug=True)