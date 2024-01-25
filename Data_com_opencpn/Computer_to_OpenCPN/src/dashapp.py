from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from multiprocessing import shared_memory
import struct

anchor_coordinates = [
    {"x0": 0, "y0": 0},
    {"x1": 0, "y1": 800},
    {"x2": 300, "y2": 800},
    {"x3": 300, "y3": 0},
]
# Assuming anchor_coordinates is a list of dictionaries like [{'x0': 0, 'y0': 0}, {'x1': 0, 'y1': 800}, ...]
# Get the maximum x value from the anchor coordinates
max_x = max(coord[f"x{i}"] for i, coord in enumerate(anchor_coordinates))

# Get the maximum y value from the anchor coordinates
max_y = max(coord[f"y{i}"] for i, coord in enumerate(anchor_coordinates))


# Convert anchor_coordinates to a DataFrame
anchor_df = pd.DataFrame(
    [(coord[f"x{i}"], coord[f"y{i}"]) for i, coord in enumerate(anchor_coordinates)],
    columns=["x", "y"],
)

# Add the first point to the end to close the loop
anchor_df = anchor_df._append(anchor_df.iloc[0], ignore_index=True)

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
test_x = [50]
test_y = [10]

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
            id="interval-component", interval=1 * 5, n_intervals=0  # in milliseconds
        ),
    ]
)


# Callback to update the Aquabot's position
@app.callback(
    Output("aquabot-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_aquabot_position(n):
    # Read coordinates from shared memory
    # Update the figure
    try:
        # Attach to the existing shared memory block
        shm = shared_memory.SharedMemory(name="coords_shm")
        # Read coordinates from shared memory
        x, y = struct.unpack("dd", shm.buf[:16])  # Assuming double precision floats
        shm.close()  # Close the shared memory block

        fig.data[-1].x = [x]
        fig.data[-1].y = [y]

        return fig
    except FileNotFoundError:
        return "Shared memory not found. Is the producer script running?"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run_server(debug=True)
