import plotly.graph_objects as go
import base64
from io import BytesIO

def create_gauge(score):
    color = "green" if score >= 70 else "orange" if score >= 40 else "red"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color},
               'steps': [{'range': [0, 40], 'color': 'red'},
                         {'range': [40, 70], 'color': 'orange'},
                         {'range': [70, 100], 'color': 'green'}]}))
    fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
    buf = BytesIO()
    fig.write_image(buf, format="png")
    return base64.b64encode(buf.getvalue()).decode('utf-8')
