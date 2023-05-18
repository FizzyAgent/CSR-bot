import streamlit as st

from api.driver.formatter import format_customer_input
from models.messages import Message, Role


def init_states():
    if "company_name" not in st.session_state:
        st.session_state["company_name"] = ""
        st.session_state["chat_messages"] = []
        st.session_state["interface_messages"] = []


def get_chat_messages() -> list[Message]:
    return st.session_state.chat_messages


def save_customer_message(message: Message) -> None:
    assert message.role == Role.customer
    st.session_state.chat_messages.append(message)
    st.session_state.interface_messages.append(format_customer_input(text=message.text))


def get_interface_messages() -> list[Message]:
    return st.session_state.interface_messages


def append_interface_message(message: Message) -> None:
    st.session_state.interface_messages.append(message)
