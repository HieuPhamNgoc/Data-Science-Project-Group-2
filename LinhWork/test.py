import plotly.express as px
import pycountry

import numpy as np
iso3_to_iso2 = {c.alpha_3: c.alpha_2 for c in pycountry.countries}

df = px.data.gapminder().query("year==2007")
df["iso_alpha2"] = df["iso_alpha"].map(iso3_to_iso2)

fig = px.scatter(
    df,
    x="lifeExp",
    y="gdpPercap",
    hover_name="country",
    hover_data=["lifeExp", "gdpPercap", "pop"],
)
fig.update_traces(marker_color="rgba(0,0,0,0)")

minDim = df[["lifeExp", "gdpPercap"]].max().idxmax()
maxi = df[minDim].max()
for i, row in df.iterrows():
    country_iso = row["iso_alpha2"]
    fig.add_layout_image(
        dict(
            source=f"https://raw.githubusercontent.com/matahombres/CSS-Country-Flags-Rounded/master/flags/{country_iso}.png",
            xref="x",
            yref="y",
            xanchor="center",
            yanchor="middle",
            x=row["lifeExp"],
            y=row["gdpPercap"],
            sizex=np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.15 + maxi * 0.03,
            sizey=np.sqrt(row["pop"] / df["pop"].max()) * maxi * 0.15+ maxi * 0.03,
            sizing="contain",
            opacity=0.8,
            layer="above"
        )
    )

fig.update_layout(height=600, width=1000, plot_bgcolor="#dfdfdf", yaxis_range=[-5e3, 55e3])

fig.show()