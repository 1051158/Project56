from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Your anchor_coordinates
anchor_coordinates = [
    {"xA0": 0, "yA0": 0},
    {"xA1": 500, "yA1": 0},
    {"xA2": 500, "yA2": 500},
    {"xA3": 1000, "yA3": 500},
    {"xA4": 1000, "yA4": 1000},
    {"xA5": 0, "yA5": 1000},
]

# Extracting maximum x and y values
max_x = max(coord[f"xA{i}"] for i, coord in enumerate(anchor_coordinates))
max_y = max(coord[f"yA{i}"] for i, coord in enumerate(anchor_coordinates))

# Convert anchor_coordinates to a DataFrame
anchor_df = pd.DataFrame(
    [(coord[f"xA{i}"], coord[f"yA{i}"]) for i, coord in enumerate(anchor_coordinates)],
    columns=["x", "y"],
)

# Add the first point to the end to close the loop
anchor_df = anchor_df.append(anchor_df.iloc[0], ignore_index=True)

# Create a Plotly Express line figure
fig = px.line(anchor_df, x="x", y="y", markers=True)

# Customize the figure
fig.update_traces(marker=dict(size=10, color="red"), line=dict(color="blue"))
fig.update_layout(
    title="Aquabot Positioning",
    xaxis_range=[0 - 100, max_x + 100],
    yaxis_range=[0 - 100, max_y + 100],
    yaxis=dict(scaleanchor="x", scaleratio=1, showticklabels=False, title=""),
    xaxis=dict(constrain="domain", showticklabels=False, title=""),
    plot_bgcolor="rgba(0,0,0,0)",
)

# Start the Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="example-graph",
            figure=fig,
            style={
                "height": "750px",
            },
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
