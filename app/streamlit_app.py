"""
streamlit_app.py

Test streamilit application for the agent.
"""

from openai import OpenAI
import streamlit as st
import agent as ag
from random import randint


if "start_config" not in st.session_state:
    st.session_state.start_config = True


if st.session_state.start_config:
    st.session_state.start_config = False
    st.session_state.id = randint(0, 1000000)
    st.session_state.graph = ag.build_graph()
    st.session_state.graph_config = {"configurable": {"thread_id": str(st.session_state.id)}}
    st.session_state.messages : list[tuple[str,object]] = [
        ("ai",
        ag.chat_welcome(
                st.session_state.graph,
                st.session_state.graph_config
            )
        )]



st.title("💬 Car assistant")

result = {}
# collect user input
if user_message := st.chat_input():
    st.session_state.messages.append(("user", user_message))
    result = ag.chat_iteration(
        user_message,
        st.session_state.graph,
        st.session_state.graph_config
       )
    messages = result.get("messages")
    ai_message = messages[-1].content
    st.session_state.messages.append(("AI", ai_message))


# list all messages stored in app session - not in langgraph state
# this is used only for displaying purpose
for msg in st.session_state.messages:
    with st.chat_message(msg[0]):
        st.write(msg[1])


def reset_session():
    st.session_state.start_config = True


with st.sidebar:
    with st.form(key="session", border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"session id:")
        with col2:
            st.write(st.session_state.id)
        st.form_submit_button(label="reset", on_click=reset_session )

    st.write("car preference:")
    st.write(result.get("car_preference", None))

    st.write("summary:")
    summary = result.get("summary", None)

    st.write({"content" : summary.content} if summary else summary)
    messages = result.get("messages", [])

    st.write(f"mesages in langgraph state [{len(messages)}]:")
    st.write(messages)

    st.write("result from invoking the graph:")
    st.write(result)



