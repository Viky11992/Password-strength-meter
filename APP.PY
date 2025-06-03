import streamlit as st
import re
import random
import string


def generate_strong_password(length=12):
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")

    remaining = length - 4
    others = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(remaining))

    password_list = list(uppercase + lowercase + digit + special + others)
    random.shuffle(password_list)
    return ''.join(password_list)


blacklist = [
    "password", "123456", "123456789", "qwerty", "abc123", "password123"
    
]


def password_strength(password):
    feedback = []
    score = 0


    if password.lower() in blacklist:
        feedback.append("❌ This password is too common. Avoid using popular passwords.")
        score -= 3


    if len(password) >= 8:
        score += 2
    else:
        feedback.append("🔸 Password should be at least 8 characters.")


    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("🔸 Add at least one uppercase letter.")


    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔸 Add at least one lowercase letter.")


    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔸 Add at least one digit.")


    if re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/]", password):
        score += 2
    else:
        feedback.append("🔸 Add at least one special character.")

    if score <= 2:
        strength = "Very Weak"
    elif 3 <= score <= 4:
        strength = "Weak"
    elif 5 <= score <= 6:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, feedback

st.title("🔐 Password Strength Checker (Weighted Score)")
st.write("Enter a password to evaluate its strength using custom scoring.")

user_password = st.text_input("🔑 Enter Password", type="password")

if user_password:
    strength, suggestions = password_strength(user_password)

    if strength == "Very Weak":
        st.error("❌ Very Weak Password")
    elif strength == "Weak":
        st.warning("⚠️ Weak Password")
    elif strength == "Moderate":
        st.info("ℹ️ Moderate Password")
    else:
        st.success("✅ Strong Password")

    if suggestions:
        st.subheader("💡 Suggestions:")
        for tip in suggestions:
            st.write(f"- {tip}")

    if strength in ["Very Weak", "Weak"]:
        st.subheader("🔑 Suggested Strong Password:")
        st.code(generate_strong_password(), language="text")
