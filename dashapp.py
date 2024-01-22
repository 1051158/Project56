from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import random

anchor_coordinates = [
    {"xA0": 0, "yA0": 0},
    {"xA1": 400, "yA1": 0},
    {"xA2": 400, "yA2": 400},
    {"xA3": 0, "yA3": 400},
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

# Create labels for each anchor point and repeat the first label at the end
labels = [f"A{i}" for i in range(len(anchor_coordinates))] + ["A0"]

# Create a Plotly Express line figure with text labels
fig = px.line(anchor_df, x="x", y="y", text=labels, markers=True)

# Customize the figure
fig.update_traces(marker=dict(size=10, color="red"), line=dict(color="blue"))
fig.update_traces(textposition="top left")
fig.update_layout(
    title="Aquabot Positioning",
    xaxis_range=[0 - 100, max_x + 100],
    yaxis_range=[0 - 100, max_y + 100],
    yaxis=dict(scaleanchor="x", scaleratio=1, showticklabels=False, title=""),
    xaxis=dict(constrain="domain", showticklabels=False, title=""),
    plot_bgcolor="rgba(0,0,0,0)",
)
test_x = [100]
test_y = [300]

fig.add_trace(
    go.Scatter(
        x=test_x,
        y=test_y,
        mode="markers",
        marker=dict(size=20, color="green"),
        name="Aquabot",
    )
)

# Start the Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="aquabot-graph",
            figure=fig,
            style={
                "height": "750px",
            },
        ),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
    ]
)


# Callback to update the Aquabot's position
@app.callback(
    Output("aquabot-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_aquabot_position(n):
    # Distances from each anchor
    distances = [77, 229, 356, 303]

    # Calculate the x and y coordinates
    x = (distances[1] ** 2 - distances[0] ** 2 + max_x**2) / (2 * max_x)
    y = (distances[3] ** 2 - distances[2] ** 2 + max_y**2) / (2 * max_y)

    # Update the figure
    fig.data[-1].x = [x]
    fig.data[-1].y = [y]

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
