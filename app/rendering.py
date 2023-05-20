from streamlit.delta_generator import DeltaGenerator

from models.messages import Message


def render_left_message(delta: DeltaGenerator, message: Message):
    text = message.text.replace("\n", "  \n")
    delta.markdown(f"**{message.role.humanized}**:  \n{text}")


def render_right_message(delta: DeltaGenerator, message: Message):
    text = message.text.replace("\n", "<br>")
    delta.markdown(
        f'<div style="text-align: right;"><strong>{message.role.humanized}:</strong><br>{text}</div>',
        unsafe_allow_html=True,
    )
