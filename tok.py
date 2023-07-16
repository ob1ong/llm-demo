import tkinter as tk
from tkinter import ttk
import os
import openai
from dataclasses import dataclass, asdict
import json
from typing import Optional, Tuple, List, Union, Literal
from textwrap import dedent
    
MODEL = "gpt-3.5-turbo"

openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class Message:
    """A class that represents a message in a ChatGPT conversation.
    """
    content: str
    role: Literal["user", "system", "assistant"]

    # is a built-in method for dataclasses
    # called after the __init__ method
    def __post_init__(self):
        self.content = dedent(self.content).strip()
        
START_CONVERSATION = [
    Message("""
        Respond with text followed by a short descriptive title for the response as a JSON formatted string of the form {"body": "body text", "title", "title text"}.
    """, role="system")
]



def generate_response(context: List[Message]) -> dict:
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[asdict(c) for c in context]
    )
    # turn into a Message object
    msg = Message(**response["choices"][0]["message"])
    
    # return the text output and the new conversation
    return msg.content
    
def update_item(selected_item):
    new_text = text_box.get("1.0", tk.END).strip()
    treeview.set(selected_item, "associated_text", new_text)

def display_text(event):
    selected_item = treeview.focus()
    associated_text = treeview.item(selected_item)["values"][0]
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, associated_text)

def add_prompt():
    selected_item = treeview.focus()
    if selected_item:
        update_item(selected_item)
        associated_text = associated_entry.get()
        new_item = treeview.insert(selected_item, "end", text="Prompt", values=(associated_text,), tags=('user',))
        treeview.see(new_item)

def remove_item():
    selected_item = treeview.focus()
    if selected_item:
        treeview.delete(selected_item)
        
def duplicate_text():
    selected_item = treeview.focus()
    if selected_item:
        associated_text = treeview.item(selected_item)["values"][0]
        parent_item = treeview.parent(selected_item)
        tags = treeview.item(selected_item, 'tags')
        new_item = treeview.insert(parent_item, "end", text="version", values=(associated_text,), tags=tags)
        
def build_context(item):
    """ trace back to the tree root to build the full context of the prompt
    """
    context = []
    while item is not None and treeview.item(item).get("values"):
        text = treeview.item(item)["values"][0]
        tags = treeview.item(item, 'tags')
        print(text, tags)
        msg = Message(text, role=tags[0])
        context = [msg] + context
        item = treeview.parent(item)
        
    return context
        
def generate_text():
    selected_item = treeview.focus()
    if selected_item:
        update_item(selected_item)
        response = generate_response(build_context(selected_item))
        new_item = treeview.insert(selected_item, "end", text="response", values=(response,), tags=('assistant',))
        treeview.see(new_item)

def on_window_resize(event):
    treeview.pack(fill=tk.BOTH, expand=True)
    text_box.pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Tree of Knowledge")

# Create Treeview
treeview = ttk.Treeview(root, columns=("associated_text"))
treeview.heading("#0", text="Item")
treeview.heading("associated_text", text="Messages")
treeview.pack(fill=tk.BOTH, expand=True)
treeview.tag_configure('user', foreground='white')
treeview.tag_configure('assistant', foreground='green')

# Bind click events
treeview.bind("<<TreeviewSelect>>", display_text)
root.bind("<Configure>", on_window_resize)

# Create Text Box
text_box = tk.Text(root, height=10, width=30)
text_box.pack(fill=tk.BOTH, expand=True)

# Button to add new item
add_button = tk.Button(root, text="Add Prompt", command=add_prompt)
add_button.pack()

# Button to remove selected item
remove_button = tk.Button(root, text="Remove Item", command=remove_item)
remove_button.pack()

# Button to duplicate text as a sibling item
save_button = tk.Button(root, text="Duplicate", command=duplicate_text)
save_button.pack()

# Button to generate text
save_button = tk.Button(root, text="Generate", command=generate_text)
save_button.pack()

# Insert Treeview root prompt
new_item = treeview.insert("", "0", "initial_prompt", text="initial prompt", values=(""), tags=('user',))

root.mainloop()
