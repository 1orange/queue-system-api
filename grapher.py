import pandas as pd
import plotly.express as px

from smart_queue.analysis import CONDITION_TABLE, RESULT_PATH

ORDER_ARRAY = [
    con.name
    for con in sorted(
        [con for _, con in CONDITION_TABLE.items()],
        key=lambda x: (-x.urgency, x.burst_time),
    )
]


# print(ORDER_TABLE)

smart = pd.read_csv(
    f"{RESULT_PATH}/10000_iters_smart",
    sep=",",
    names=["condition", "wait_time"],
    header=None,
    encoding="utf8",
).assign(type="Smart")

naive = pd.read_csv(
    f"{RESULT_PATH}/10000_iters_naive",
    sep=",",
    names=["condition", "wait_time"],
    header=None,
    encoding="utf8",
).assign(type="Naive")

df = pd.concat([naive, smart])

fig = px.box(
    df,
    x="condition",
    y="wait_time",
    color="type",
    labels={
        "condition": "Condition",
        "wait_time": "Wait time (minutes)",
        "type": "Queue type",
    },
    title="NAIVE vs SMART - Random amount of patients (10 000 iterations)",
)

for con in df.condition.unique():
    fig.add_annotation(
        x=con,
        y=df[df["condition"] == con]["wait_time"].max() + 10,
        text=f'n={str(len(df[df["condition"] == con]["wait_time"]))}',
        yshift=5,
        showarrow=False,
    )

fig.update_xaxes(categoryorder="array", categoryarray=ORDER_ARRAY)

fig.update_layout(
    font=dict(family="Courier New, Monospace", size=18, color="#000000")
)

fig.show()
