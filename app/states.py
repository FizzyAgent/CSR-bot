import streamlit as st

from api.driver.formatter import format_customer_input
from api.models.messages import Message, Role
from api.models.program_loader import ProgramLoader
from api.models.resource_loader import ResourceLoader


def init_states():
    if "company_name" not in st.session_state:
        st.session_state["company_name"] = ""
        st.session_state["chat_messages"] = []
        st.session_state["interface_messages"] = []
        st.session_state["resource_loader"] = ResourceLoader()
        st.session_state["program_loader"] = ProgramLoader()


def get_all_companies() -> list[str]:
    return st.session_state.resource_loader.get_all_companies()


def set_company_name(company_name) -> None:
    st.session_state.resource_loader.set_company(company_name=company_name)
    st.session_state.program_loader.set_company(company_name=company_name)


def get_resource_loader() -> ResourceLoader:
    return st.session_state.resource_loader


def get_program_loader() -> ProgramLoader:
    return st.session_state.program_loader


def get_chat_messages() -> list[Message]:
    return st.session_state.chat_messages


def save_customer_message(message: Message) -> None:
    assert message.role == Role.customer
    st.session_state.chat_messages.append(message)
    interface_message = Message(
        role=Role.app,
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
