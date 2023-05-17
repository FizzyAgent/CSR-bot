import streamlit as st

from app.models import Role, Message
from app.rendering import render_left_msg, render_right_msg
from app.states import init_states, get_chat_msgs, get_interface_msgs, append_chat_msg

st.set_page_config(page_title="CSRbot Demo", layout="wide")
init_states()

left, right = st.columns(2)

with left:
    st.markdown("### Behind the scenes of CSRbot")
    interface_msgs = get_interface_msgs()
    for msg in interface_msgs:
        if msg.role == Role.bot:
            render_right_msg(delta=left, msg=msg)
        elif msg.role == Role.system:
            render_left_msg(delta=left, msg=msg)

with right:
    st.markdown("### Chat with CSRbot")
    chat_msgs = get_chat_msgs()
    for msg in chat_msgs:
        if msg.role == Role.customer:
            render_right_msg(delta=right, msg=msg)
        elif msg.role == Role.bot:
            render_left_msg(delta=right, msg=msg)
    new_input = st.text_area(
        label="Message Box",
        label_visibility="hidden",
        key=f"message_input_{len(chat_msgs)}",
    )
    if st.button("Submit") and new_input:
        new_msg = Message(role=Role.customer, text=new_input)
        append_chat_msg(msg=new_msg)
        st.experimental_rerun()
