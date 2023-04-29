import streamlit as st
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import io

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

