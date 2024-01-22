from dash import Dash, html, dcc, Output, Input
import plotly.graph_objects as go
from pymongo import MongoClient
import ast

uri = "mongodb+srv://aleniriskic:0hZpyfFParfakoMe@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.RangeData

collection = db["trip1"]
entries = collection.find()

# Extracting the 'range' field from each entry and converting it to a string
ranges = [str(entry["range"]) for entry in entries]

distance_from_a0 = []
distance_from_a1 = []
distance_from_a2 = []
distance_from_a3 = []

for range_str in ranges:
    range_list = ast.literal_eval(range_str)
    if range_list:
        distance_from_a0.append(range_list[0])
        distance_from_a1.append(range_list[1])
        distance_from_a2.append(range_list[2])
        distance_from_a3.append(range_list[3])

# Joining the ranges with line breaks
ranges_html = " ".join(ranges)

anchor_coordinates = [
    {"xA0": 0, "yA0": 0},
    {"xA1": 1000, "yA1": 0},
    {"xA2": 1000, "yA2": 1000},
    {"xA3": 0, "yA3": 1000},
]

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(
            id="graph-content",
            style={
                "height": "750px",
            },
        ),
    ]
)


@app.callback(Output("graph-content", "figure"), Input("graph-content", "id"))
def update_graph(id):
    anchor = {
        "xA0": anchor_coordinates[0]["xA0"],
        "yA0": anchor_coordinates[0]["yA0"],
        "xA1": anchor_coordinates[1]["xA1"],
        "yA1": anchor_coordinates[1]["yA1"],
        "xA2": anchor_coordinates[2]["xA2"],
        "yA2": anchor_coordinates[2]["yA2"],
        "xA3": anchor_coordinates[3]["xA3"],
        "yA3": anchor_coordinates[3]["yA3"],
    }

    max_x = max([anchor.get(f"xA{i}", 0) for i in range(4)])
    max_y = max([anchor.get(f"yA{i}", 0) for i in range(4)])

    anchor_points_x = [anchor[f"xA{i}"] for i in range(4)]
    anchor_points_y = [anchor[f"yA{i}"] for i in range(4)]
    anchor_labels = [f"A{i}" for i in range(4)]

    fig = go.Figure()

    # Plotting the bounding box
    fig.add_trace(
        go.Scatter(
            x=[0, max_x, max_x, 0, 0],
            y=[0, 0, max_y, max_y, 0],
            mode="lines",
            name="Border",
        )
    )

    # Adding anchor points
    fig.add_trace(
        go.Scatter(
            x=anchor_points_x,
            y=anchor_points_y,
            mode="markers",
            name="Anchor Points",
            marker=dict(size=10, color="red"),
        )
    )

    # Manually setting the position of the labels outside the bounding box
    text_offset = 50  # Adjust this value to move the labels further from the box
    label_positions_x = [
        x - text_offset if x == 0 else x + text_offset for x in anchor_points_x
    ]
    label_positions_y = [
        y - text_offset if y == 0 else y + text_offset for y in anchor_points_y
    ]

    # Adding labels as separate traces
    for label, x, y in zip(anchor_labels, label_positions_x, label_positions_y):
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                text=[label],
                mode="text",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Aquabot Positioning",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(scaleanchor="x", scaleratio=1, showticklabels=False),
        xaxis=dict(constrain="domain", showticklabels=False),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
