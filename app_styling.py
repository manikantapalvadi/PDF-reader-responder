# Store CSS as a string
css = '''
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
    }
    .chat-message.user {
        background-color: #dcdaf1;
    }
    .chat-message.bot {
        background-color:#e5e3f4;
    }
    .chat-message .avatar {
        width: 15%;
    }
    .chat-message .avatar img {
        max-width: 50px;
        max-height: 50px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 85%;
        padding:0 1.5rem;
        color: #403d39;
    }
</style>
'''

# Store bot template as a string
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqgARKy__ewikuT7TqVsDASVzEr4HN-DSrfA&s">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# Store user template as a string
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/png;base64,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">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# Example usage with Streamlit
import streamlit as st

def main():
    st.markdown(css, unsafe_allow_html=True)

    user_message = user_template.replace("{{MSG}}", "Hello, this is a user message!")
    bot_message = bot_template.replace("{{MSG}}", "Hi there, this is a bot message!")

    st.markdown(user_message, unsafe_allow_html=True)
    st.markdown(bot_message, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
