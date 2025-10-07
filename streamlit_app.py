import streamlit as st
import replicate
import tempfile
import os

# --- CONFIG ---
# Replicate model (DeOldify for video)
REPLICATE_MODEL = "arielreplicate/deoldify_video:8f2ec49a728e6e0cd8e61b7fdbac0cc65a8476a96c44ab15635c9248d9fc0c29"

# Read API key from Streamlit secrets
API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

# --- STREAMLIT APP ---
st.title("🎥 AI Video Colorizer")
st.write("Upload a short black & white video and let AI bring it to life in color!")

uploaded_file = st.file_uploader("Choose a video", type=["mp4", "mov", "avi"])

if uploaded_file:
    # Save uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        bw_path = tmp.name

    st.subheader("Original Black & White Video")
    st.video(bw_path)

    if st.button("✨ Colorize with AI"):
        with st.spinner("Colorizing... this may take 1–2 minutes ⏳"):
            client = replicate.Client(api_token=API_TOKEN)
            output_url = client.run(
                REPLICATE_MODEL,
                input={"video": open(bw_path, "rb")}
            )

        if output_url:
            st.success("Done! Here's the result:")
            st.video(output_url)

            # Toggle viewer
            option = st.radio("View Mode:", ["Black & White", "Colorized"])
            if option == "Black & White":
                st.video(bw_path)
            else:
                st.video(output_url)
