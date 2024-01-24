from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from pymongo import MongoClient
import certifi


anchor_coordinates = [
    {"xA0": 0, "yA0": 0},
    {"xA1": 580, "yA1": 0},
    {"xA2": 580, "yA2": 550},
    {"xA3": 0, "yA3": 550},
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
anchor_df = anchor_df._append(anchor_df.iloc[0], ignore_index=True)
# anchor_df = anchor_df.append(anchor_df.iloc[0], ignore_index=True)

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
test_x = [120]
test_y = [100]

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
            id="interval-component", interval=1 * 740, n_intervals=0  # in milliseconds
        ),
    ]
)


# Function to calculate the Aquabot's position using the three-point algorithm
def calculate_aquabot_position(distance_from_A0, distance_from_A1, distance_from_A2):
    # Coordinates of the anchor points
    xA0, yA0 = anchor_df.iloc[0]
    xA1, yA1 = anchor_df.iloc[1]
    xA2, yA2 = anchor_df.iloc[2]

    # Calculate the Aquabot's position
    x = (distance_from_A0**2 - distance_from_A1**2 + xA1**2) / (2 * xA1)
    y = (
        distance_from_A0**2
        - distance_from_A2**2
        + xA2**2
        + yA2**2
        - 2
        * yA2
        * ((distance_from_A0**2 - distance_from_A1**2 + xA1**2) / (2 * xA1))
    ) / (2 * yA2)

    return x, y


# Callback to update the Aquabot's position
@app.callback(
    Output("aquabot-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_aquabot_position(n):
    distance_from_anchors = get_coordinates_from_db()

    # Distances from each anchor
    distance_from_A0 = int(distance_from_anchors[0][0])
    distance_from_A1 = int(distance_from_anchors[0][1])
    distance_from_A2 = int(distance_from_anchors[0][2])

    # Calculate the Aquabot's position
    x, y = calculate_aquabot_position(
        distance_from_A0, distance_from_A1, distance_from_A2
    )

    # Update the figure
    fig.data[-1].x = [x]
    fig.data[-1].y = [y]

    return fig


def get_coordinates_from_db():
    uri = "mongodb+srv://aleniriskic:lr9iu3bI3WtRXLJa@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client.RangeData

    collection = db["trip1"]
    entries = collection.find()

    # Assuming you want the last three ranges
    ranges = [entry["range"] for entry in entries][-1:]

    return ranges


if __name__ == "__main__":
    app.run_server(debug=True)
