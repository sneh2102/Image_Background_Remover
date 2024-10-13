import streamlit as st
from rembg import remove
from PIL import Image
import io
import numpy as np

# Function to apply a threshold to the image
def apply_threshold(image: Image, threshold: int) -> Image:
    # Convert the image to a numpy array
    image_array = np.array(image)
    
    # Create a mask based on the threshold
    mask = (image_array[:, :, 3] < threshold)  # Assuming the alpha channel is the 4th channel
    
    # Apply the mask to the image
    image_array[mask] = [0, 0, 0, 0]  # Set the masked pixels to transparent

    return Image.fromarray(image_array)

# Streamlit app title
st.title("Background Remover App with Threshold Adjustment")

# File uploader widget to upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Slider for threshold adjustment
threshold = st.slider("Select Threshold", 0, 255, 128)

# If an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Convert the uploaded file to bytes
    img_bytes = uploaded_file.read()

    # Remove background
    output_img_bytes = remove(img_bytes)

    # Convert the result back to an image format
    output_image = Image.open(io.BytesIO(output_img_bytes))

    # Apply threshold to the output image
    thresholded_image = apply_threshold(output_image, threshold)

    # Display the thresholded result image
    st.image(thresholded_image, caption="Image with Background Removed and Threshold Applied", use_column_width=True)

    # Prepare the result image for download
    buf = io.BytesIO()
    thresholded_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Provide a download button
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="background_removed_with_threshold.png",
        mime="image/png"
    )
