import streamlit as st
import requests
import json

# Initialize session state for messages and tool list if not already set
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_role' not in st.session_state:
    st.session_state.current_role = "user"
if 'function_name' not in st.session_state:
    st.session_state.function_name = ""
if 'argument' not in st.session_state:
    st.session_state.argument = ""
if 'tool_call_id' not in st.session_state:
    st.session_state.tool_call_id = ""
if 'content' not in st.session_state:
    st.session_state.content = ""

# Function to send data to the model
def send_to_model():
    url = 'https://openai-dev-fra-001.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-21'
    headers = {
        'api-key': '28dd324b1b444e88aa6f3f1d9d310d6d',
        'Content-Type': 'application/json'
    }
    # Prepare messages with correct tool_calls and tool_call_id
    messages = []
    for message in st.session_state.messages:
        msg = {"role": message['role']}
        if 'content' in message and message['content'] is not None:
            msg["content"] = message['content']
        if 'tool_calls' in message:
            msg["tool_calls"] = message['tool_calls']
        if 'tool_call_id' in message:
            msg["tool_call_id"] = message['tool_call_id']
        messages.append(msg)
    data = {
        "model": "gpt-4o",
        "messages": messages,
        "tools": json.loads(st.session_state.tools_json) if st.session_state.tools_json else []
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data:
            return response_data["choices"][0]["message"]["content"]
        else:
            st.error(f"Expected data format not found in response: {response_data}")
    else:
        st.error(f"Failed to get valid response. Status Code: {response.status_code}, Response: {response.text}")
    return "Error or different response format"

# App layout
st.title('Messages builder for OpenAI API')

# Role selectbox outside the form to allow dynamic updates
role = st.selectbox("Select role for new message", ["user", "system", "assistant - response", "assistant - tool_call", "tool"], key='new_role')
st.session_state.current_role = role

# Reset variables based on selected role
if "assistant - tool_call" in st.session_state.current_role:
    st.session_state.function_name = st.text_input("Function name", value=st.session_state.function_name)
    st.session_state.argument = st.text_input("Argument value for 'name'", value=st.session_state.argument)
    st.session_state.tool_call_id = st.text_input("Tool Call ID", value=st.session_state.tool_call_id)
    # Reset other variables
    st.session_state.content = ""
elif "tool" in st.session_state.current_role:
    st.session_state.tool_call_id = st.text_input("Tool Call ID", value=st.session_state.tool_call_id)
    st.session_state.content = st.text_area("Message content", value=st.session_state.content)
    # Reset other variables
    st.session_state.function_name = ""
    st.session_state.argument = ""
else:
    st.session_state.content = st.text_area("Message content", value=st.session_state.content)
    # Reset other variables
    st.session_state.function_name = ""
    st.session_state.argument = ""
    st.session_state.tool_call_id = ""

# Form to capture the current state of fields
with st.form("message_form"):
    # No need for hidden/disabled fields
    # Just a submit button
    submitted = st.form_submit_button("Add Message")
    if submitted:
        if "assistant - tool_call" in st.session_state.current_role:
            if st.session_state.function_name and st.session_state.argument and st.session_state.tool_call_id:
                tool_call_id = st.session_state.tool_call_id
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call_id,
                        "type": "function",
                        "function": {
                            "name": st.session_state.function_name,
                            "arguments": json.dumps({"name": st.session_state.argument})
                        }
                    }]
                })
            else:
                st.error("Function name, argument, and tool_call_id are required for 'assistant - tool_call' role.")
        elif "tool" in st.session_state.current_role:
            if st.session_state.content and st.session_state.tool_call_id:
                st.session_state.messages.append({
                    "role": "tool",
                    "content": st.session_state.content,
                    "tool_call_id": st.session_state.tool_call_id
                })
            else:
                st.error("Content and Tool Call ID are required for 'tool' role.")
        else:
            if st.session_state.content:
                st.session_state.messages.append({
                    "role": st.session_state.current_role,
                    "content": st.session_state.content
                })
            else:
                st.error("Content is required for this role.")

# Display and edit messages dynamically
for index, message in enumerate(st.session_state.messages):
    with st.expander(f"Message {index + 1} ({message['role']}):"):
        if 'tool_calls' in message:
            editable_role = "assistant - tool_call"
        else:
            editable_role = message['role']
        
        editable_role = st.selectbox(
            f"Role for message {index + 1}",
            ["user", "system", "assistant - response", "assistant - tool_call", "tool"],
            index=["user", "system", "assistant - response", "assistant - tool_call", "tool"].index(editable_role),
            key=f'role_{index}'
        )
        
        if "assistant - tool_call" in editable_role:
            function_name = st.text_input("Function name", value=message.get('tool_calls', [{}])[0].get('function', {}).get('name', ''), key=f'function_name_{index}')
            argument = st.text_input("Argument value for 'name'", value=json.loads(message.get('tool_calls', [{}])[0].get('function', {}).get('arguments', '{}')).get('name', ''), key=f'argument_{index}')
            tool_call_id = st.text_input("Tool Call ID", value=message.get('tool_calls', [{}])[0].get('id', ''), key=f'tool_call_id_{index}')
            content = None
        elif "tool" in editable_role:
            content = st.text_area("Message content", value=message.get('content', ''), key=f'content_{index}')
            tool_call_id = st.text_input("Tool Call ID", value=message.get('tool_call_id', ''), key=f'tool_call_id_{index}')
            function_name = None
            argument = None
        else:
            content = st.text_area("Message content", value=message.get('content', ''), key=f'content_{index}')
            function_name = None
            argument = None
            tool_call_id = None
        
        if st.button("Save Changes", key=f'save_{index}'):
            if "assistant - tool_call" in editable_role:
                if function_name and argument and tool_call_id:
                    message['role'] = "assistant"
                    message['content'] = None
                    message['tool_calls'] = [{
                        "id": tool_call_id,
                        "type": "function",
                        "function": {
                            "name": function_name,
                            "arguments": json.dumps({"name": argument})
                        }
                    }]
                else:
                    st.error("Function name, argument, and tool_call_id are required for 'assistant - tool_call' role.")
            elif "tool" in editable_role:
                if content and tool_call_id:
                    message['role'] = "tool"
                    message['content'] = content
                    message['tool_call_id'] = tool_call_id
                else:
                    st.error("Content and Tool Call ID are required for 'tool' role.")
            else:
                if content:
                    message['role'] = editable_role
                    message['content'] = content
                    if 'tool_calls' in message:
                        del message['tool_calls']
                    if 'tool_call_id' in message:
                        del message['tool_call_id']
                else:
                    st.error("Content is required for this role.")
        
        if st.button("Delete", key=f'delete_{index}'):
            st.session_state.messages.pop(index)

# Tools JSON input
st.text_area("Paste Tool List JSON here", key='tools_json', height=150)

# Send to model button
if st.button('Send to Model'):
    response = send_to_model()
    st.write("### Model Response")
    st.write(response)