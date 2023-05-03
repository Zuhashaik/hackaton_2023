import streamlit as st
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import io

st.title("Image Uploader")

st.header("Upload an Image")

image_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if image_file is not None:
    image_bytes = io.BytesIO(image_file.read())

    pipeline = keras_ocr.pipeline.Pipeline()
    images = keras_ocr.tools.read(image_bytes)
    images = images.reshape((-1,) + images.shape)

    prediction_groups = pipeline.recognize(images)

    text_predictions = []
    for predictions in prediction_groups:
        prediction_text = []
        for word in predictions:
            prediction_text.append(word[0])
        text_predictions.append(" ".join(prediction_text))
        
    st.subheader("Annotated Image with Text Predictions")
    fig, axs = plt.subplots(nrows=len(images), figsize=(10, 20))
    axs_flat = np.ravel(axs)
    for ax, image, predictions in zip(axs_flat, images, prediction_groups):
        ax.imshow(image)
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
        ax.axis("off")
    st.pyplot(fig)

    st.subheader("Text Predictions")
    st.write("\n".join(text_predictions))

