import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from api.models.messages import Message


def render_style() -> None:
    st.markdown(
        """
        <style>
        .appview-container{
            display: flex;
            justify-content: space-between;
        }
        section[data-testid='stSidebar'][aria-expanded='true']>:first-child {
            width: 100%;
        }
        /* Sidebar takes up 3 portions of width */
        .appview-container > :first-child {
            flex: 3;
            max-width: 100%;
        }
        /* Right side takes up 2 portions of width */
        .appview-container > :nth-child(2) {
            flex: 2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_left_message(delta: DeltaGenerator, message: Message) -> None:
    text = message.text.replace("\n", "  \n").replace("$", "\$")
    delta.markdown(f"**{message.role.humanized}**:  \n{text}")


def render_right_message(delta: DeltaGenerator, message: Message) -> None:
    text = message.text.replace("\n", "<br>")
    delta.markdown(
        f'<div style="text-align: right;"><strong>{message.role.humanized}:</strong><br>{text}</div>',
        unsafe_allow_html=True,
    )
