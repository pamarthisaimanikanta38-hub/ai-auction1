import graphviz
import streamlit as st

def show_tree():

    dot = graphviz.Digraph()

    dot.node("A","Start Bid")
    dot.node("B","Team Value")
    dot.node("C","Bid")
    dot.node("D","Pass")

    dot.edge("A","B")
    dot.edge("B","C","High Value")
    dot.edge("B","D","Low Value")

    st.graphviz_chart(dot)