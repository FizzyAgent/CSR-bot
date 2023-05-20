import streamlit as st
from iso3166 import countries

from api.driver.logic_service import run
from models.messages import Role, Message
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
from models.settings import ChatSettings

st.set_page_config(page_title="CSR Bot Demo", layout="wide")
init_states()

with st.sidebar:
    st.markdown("**Settings**")
    company = st.selectbox(label="Select a Company", options=get_all_companies())
    set_company_name(company_name=company)
    location = st.selectbox(
        label="Your Location",
        options=[c.name for c in countries],
    )
    settings = ChatSettings(
        company=company,
        location=location,
        resource_loader=get_resource_loader(),
        program_loader=get_program_loader(),
    )


left, right = st.columns(2)

with left:
    st.markdown("### Behind the scenes of CSRbot")
    interface_messages = get_interface_messages()
    for message in interface_messages:
        if message.role == Role.bot:
            render_right_message(delta=left, message=message)
        elif message.role == Role.app:
            render_left_message(delta=left, message=message)

with right:
    st.markdown("### Chat with CSRbot")
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
    if st.button("Submit") and new_input:
        new_message = Message(role=Role.customer, text=new_input)
        save_customer_message(message=new_message)
        st.experimental_rerun()

if len(interface_messages) > 0 and interface_messages[-1].role != Role.bot:
    run(messages=interface_messages, settings=settings)
    st.experimental_rerun()
