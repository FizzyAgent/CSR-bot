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
    interface_message = Message(
        role=Role.system,
        text=format_customer_input(text=message.text),
    )
    st.session_state.interface_messages.append(interface_message)


def save_bot_message(message: Message) -> None:
    assert message.role == Role.bot
    st.session_state.chat_messages.append(message)


def get_interface_messages() -> list[Message]:
    return st.session_state.interface_messages


def save_interface_message(message: Message) -> None:
    st.session_state.interface_messages.append(message)
