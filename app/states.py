import streamlit as st

from app.models import Message


def init_states():
    if "company_name" not in st.session_state:
        st.session_state["company_name"] = ""
        st.session_state["chat_msgs"] = []
        st.session_state["interface_msgs"] = []


def get_chat_msgs() -> list[Message]:
    return st.session_state.chat_msgs


def append_chat_msg(msg: Message) -> None:
    st.session_state.chat_msgs.append(msg)


def get_interface_msgs() -> list[Message]:
    return st.session_state.interface_msgs


def append_interface_msg(msg: Message) -> None:
    st.session_state.interface_msgs.append(msg)
