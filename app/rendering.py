from streamlit.delta_generator import DeltaGenerator

from models.messages import Message


def render_left_message(delta: DeltaGenerator, message: Message):
    delta.markdown(f"{message.role.humanized}:  \n{message.text}")


def render_right_message(delta: DeltaGenerator, message: Message):
    delta.markdown(
        f'<div style="text-align: right;">{message.role.humanized}:</div>'
        f'<div style="text-align: right;">{message.text}</div>',
        unsafe_allow_html=True,
    )
