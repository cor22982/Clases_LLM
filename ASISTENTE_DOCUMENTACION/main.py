from backend.Core import run_llm
import streamlit as st

from streamlit_chat import message

prompt = st.text_input("Prompt", placeholder = "Enter your prompt here")

if (
    "chat_anwers_history" not in st.session_state and
    "user_prompt_history" not in st.session_state and
    "chat_history" not in st.session_state
):
    st.session_state["chat_anwers_history"]= []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

def create_sources_string(source_urls: set[str])->str:
    if not source_urls:
        return ""
    source_list = list(source_urls)
    source_list.sort()
    source_string="sources:\n"

    for i , source in enumerate(source_list):
        source_string += f"{i+1}.{source}\n"
    return source_string

if prompt:
    with st.spinner("Generating responde"):
        generated_responde = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"]
        )
        #en el fronted vamos a mostrar la respuesta, y otro es los lugares de donde los saco o links
        sources = set([doc.metadata["source"] for doc in generated_responde["source"]])
        formated_responde = f"{generated_responde['result']}\n\n{create_sources_string(sources)}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_anwers_history"].append(formated_responde)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_responde["result"]))

    if st.session_state["chat_anwers_history"]:
        for i, (generated_responde, user_query) in enumerate(
                zip(st.session_state["chat_anwers_history"], st.session_state["user_prompt_history"])):
            message(user_query, is_user=True, key=f"user_{i}")
            message(generated_responde, key=f"bot_{i}")










