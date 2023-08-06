import streamlit as st

class SessionState:
    def __init__(self):
        self._state = {}
        if not hasattr(self, "search_history"):
            self.search_history = []

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value
