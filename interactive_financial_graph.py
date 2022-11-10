import streamlit as st
import altair as alt
import pandas as pd
import numpy as np


st.set_page_config(layout="wide")
# create determined budget graph

arizona_input = st.number_input("Budget Arizona", min_value=0, max_value=3000, value=1500)
h_caro = st.number_input("Heures par semaine Caro", 0.0, 15.0, value=7.5)
cs_f = st.number_input("Heures par semaine CS reste automne", 0.0, 6.0, value=4.5)
cs_h = st.number_input("Heures par semaine CS hiver", 0.0, 6.0, value=4.5)
revenu_h = st.number_input("Nombres membres hiver", 0, 37, value=27)
financement = st.number_input("Activité de financement", 0, 2000, value=0)


bp = [10500, 9685, 8785, 5485, 4730, 3030]
#cat = ["initial", "cotisations", "casques", "Paye Caro", "Avion Caro", "Centre sud P"]


bp_futur = [np.nan] * 5 + [3030]
bp_futur.append(bp_futur[-1] + revenu_h * 300)
bp_futur.append(bp_futur[-1] - (h_caro * 55 * 14))
bp_futur.append(bp_futur[-1] - (cs_f * 50 * 5))
bp_futur.append(bp_futur[-1] + financement)
bp_futur.append(bp_futur[-1] - arizona_input)
bp_futur.append(bp_futur[-1] - (cs_h * 50 * 14))

bp = bp + [np.nan] * 6

df = pd.DataFrame({
    "danger": [2000] * 12,
    "solde": bp,
    "solde_futur": bp_futur,
})

print(df)

scale = alt.Scale(domain=['danger', 'solde', 'solde_futur'], range=['red', 'blue', 'black'])

data = df.reset_index().melt("index")
temp_chart = alt.Chart(data).mark_line().encode(
    alt.X('index', axis=alt.Axis(title="depenses", grid=False)),
    alt.Y('value', 
        axis=alt.Axis(title="solde", grid=False)),
    color = alt.Color('variable', scale=scale),
    strokeDash = alt.condition(
        alt.datum.variable == 'solde_futur',
        alt.value([5,5]),
        alt.value([0])
    )
)


# points

source = pd.DataFrame({
    'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'y': bp[0:5] + bp_futur[5:],
    'label': ["initial", "cotisations", "casques", "Paye Caro", "Avion Caro", "CS A", "Revenus hiver", "Paye Caro", "CS reste automne", "Financement", "Arizona", "CS hiver"]
})

points = alt.Chart(source).mark_point().encode(
    x='x:Q',
    y='y:Q'
)

text = points.mark_text(
    align='left',
    baseline='middle',
    dx=7
).encode(
    text='label'
)

st.altair_chart(points + text + temp_chart, use_container_width=True)
st.dataframe(df)

