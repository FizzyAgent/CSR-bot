import streamlit as st
from iso3166 import countries

from api.driver.logic_service import run
from api.models.messages import Role, Message
from app.rendering import render_left_message, render_right_message
from app.states import (
    init_states,
    get_chat_messages,
    get_interface_messages,
    save_customer_message,
    get_all_companies,
    set_company_name,
    get_resource_loader,
    get_program_loader,
)
from api.models.settings import ChatSettings

st.set_page_config(page_title="CSR Bot Demo", layout="wide")
init_states()

with st.sidebar:
    st.markdown("**Settings**")
    company = st.selectbox(label="Select a Company", options=get_all_companies())
    set_company_name(company_name=company)
    countries = [c.name for c in countries]
    location = st.selectbox(
        label="Your Location",
        options=countries,
        index=countries.index("Singapore"),
    )
    settings = ChatSettings(
        company=company,
        location=location,
        resource_loader=get_resource_loader(),
        program_loader=get_program_loader(),
    )


left, right = st.columns(2)


with left:
    st.markdown("### Behind the scenes of CSR Bot")
    interface_messages = get_interface_messages()
    for message in interface_messages:
        if message.role == Role.bot:
            render_right_message(delta=left, message=message)
        elif message.role == Role.app:
            render_left_message(delta=left, message=message)

with right:
    st.markdown("### Chat with CSR Bot")
    chat_messages = get_chat_messages()
    for message in chat_messages:
        if message.role == Role.customer:
            render_right_message(delta=right, message=message)
        elif message.role == Role.bot:
            render_left_message(delta=right, message=message)
    new_input = st.text_area(
        label="Message Box",
        label_visibility="hidden",
        key=f"message_input_{len(chat_messages)}",
    )

    def save_user_input() -> None:
        user_input = new_input.strip()
        if len(user_input) == 0:
            return
        new_message = Message(role=Role.customer, text=user_input)
        save_customer_message(message=new_message)

    st.button("Submit", on_click=save_user_input)

terminated = False
messages = get_chat_messages()
if len(messages) > 0 and messages[-1].role != Role.bot:
    while not terminated and messages[-1].role != Role.bot:
        interface_messages = get_interface_messages()
        terminated = run(messages=interface_messages, settings=settings)
        messages = get_chat_messages()
    st.experimental_rerun()
