import streamlit as st
import speech_recognition as sr
import streamlit as st
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import io
import pyttsx3

engine = pyttsx3.init()

st.title("This is a application for visually impaired individuals")
st.header("1.Text Detection Mode")
st.header("2.Object detection mode")
st.header("3.Surroundings detection Mode")

engine.say("This is an application for visually impaired individuals. There are three available modes: Text Detection Mode, Object detection mode, and Surroundings detection Mode. Please select your option by saying it aloud.")
engine.runAndWait()

def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.write(f"{text}")
        return text
    except:
        st.write("Sorry, could not recognize your voice")
        return ""

def page1():
    st.title("Text Detection from Image")
    # Title of the app
    st.title("Image Uploader")

    # A header for the section
    st.header("Upload an Image")

    # A file uploader for the image
    image_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    # If an image is uploaded, show it
    if image_file is not None:
        # Read the image file as a bytes-like object
        image_bytes = io.BytesIO(image_file.read())

        # Use keras_ocr to read the image
        pipeline = keras_ocr.pipeline.Pipeline()
        images = keras_ocr.tools.read(image_bytes)
        images = images.reshape((-1,) + images.shape)

        # Recognize text in the image
        prediction_groups = pipeline.recognize(images)

        # Extract the text predictions from the recognition results
        text_predictions = []
        for predictions in prediction_groups:
            prediction_text = []
            for word in predictions:
                prediction_text.append(word[0])
            text_predictions.append(" ".join(prediction_text))

        # Display the annotated image with the recognized text
        st.subheader("Annotated Image with Text Predictions")
        fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
        axs_flat = np.ravel(axs)
        for ax, image, predictions in zip(axs_flat, images, prediction_groups):
            ax.imshow(image)
            keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
            ax.axis("off")
        st.pyplot(fig)

        # Display the recognized text
        st.subheader("Text Predictions")
        st.write("\n".join(text_predictions))
    
# Define the function to redirect to Page 2
def page2():
    st.title("Person Detection")
    st.write("Spot the human: Person detection for a safer world")
    
# Define the function to redirect to Page 3
def page3():
    st.title("Surroundings Detection")
    st.write("Discover hidden secrets in your surroundings with cutting-edge surroundings detection technology")
if __name__ == '__main__':
    user_input = transcribe_audio()

    # Display buttons based on user input
    if user_input:
        if "text detection mode" in user_input:
            page1()
        if "object detection mode" in user_input:
            page2()
        if "surroundings detection mode" in user_input:
            page3()

