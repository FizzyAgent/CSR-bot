from streamlit.delta_generator import DeltaGenerator

from app.models import Message


def render_left_msg(delta: DeltaGenerator, msg: Message):
    delta.markdown(f"{msg.role.humanized}:  \n{msg.text}")


def render_right_msg(delta: DeltaGenerator, msg: Message):
    delta.markdown(
        f'<div style="text-align: right;">{msg.role.humanized}:</div>'
        f'<div style="text-align: right;">{msg.text}</div>',
        unsafe_allow_html=True,
    )
