import streamlit as st
from PIL import Image
import io

# Set the Page Icon and title
st.set_page_config(
    page_title="PASSPORT AND SIGNATURE TRANSFORMATION",
    page_icon="app_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed")

st.markdown("""## IMAGE TRANSFORMER""")
st.divider()

st.markdown("""
           ### `Prepare passport photographs and signatures for online applications!`
            """)

st.divider()

st.info(""" **ⓘ** _Select an image type from the sidebar to get started._ `<<<`""")

SIGN_SIZE = (200, 200)
PASSPORT_SIZE = (300, 300)


def get_file_size(file):
    size_bytes = len(file)

    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


st.sidebar.markdown("""## Image Transformation Options""")
st.sidebar.divider()

# Image transformation options
user_pref = st.sidebar.selectbox(
    "What are you transforming?",
    ["Passport Photograph",
     "Signature"]
)

st.sidebar.divider()


# Signature Upload
if user_pref == "Signature":
    signature_photograph = st.sidebar.file_uploader(
        "Upload Signature Photograph", type=["jpg", "jpeg", "png"])

    if signature_photograph:

        # open uploaded image
        signature_img = Image.open(signature_photograph)
        original_size = get_file_size(signature_photograph.getvalue())

        # Details of uploaded signature photo
        with st.container(border=True):
            st.title("Original Signature")

            col1, col2 = st.columns([1.5, 1])

            with col1:

                st.image(
                    signature_img,
                    use_container_width=True
                )

            with col2:

                st.metric(
                    "Dimensions",
                    f"{signature_img.width} × {signature_img.height}"
                )

                st.metric(
                    "File Size",
                    original_size
                )

                st.metric(
                    "Format",
                    signature_img.format
                )

        # convert the signature to thumbnail
        signature_img.thumbnail(SIGN_SIZE)

        # convert uploaded image to gray scale
        gray_image = signature_img.convert("L")

        # CONVERT PIL IMAGE TO BYTES FOR DOWNLOAD
        buf = io.BytesIO()
        gray_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # TRANSFORMATION
        transformed_bytes = buf.getvalue()

        transformed_size = get_file_size(
            transformed_bytes)

        st.success("Signature transformed successfully.")

        # DETAILS OF TRANSFORMED SIGNATURE
        with st.container(border=True):
            st.title("Transformed Signature")
            col1, col2 = st.columns([1.5, 1])

            with col1:

                st.image(
                    gray_image,
                    use_container_width=True
                )

            with col2:

                st.metric(
                    "Dimensions",
                    f"{gray_image.width} × {gray_image.height}",
                    delta_arrow="down"
                )

                st.metric(
                    "File Size",
                    transformed_size,
                    delta_arrow="down"
                )

                st.metric(
                    "Format",
                    "PNG",
                    delta_arrow="down"
                )
                

        # downloading signature photo
        st.download_button(
            label="⬇️Download the transformed signature photo",
            file_name="transformed_signature.png",
            data=byte_im,
            mime="image/png"
        )


# Passport Photograph Uplaod
else:
    passport_photograph = st.sidebar.file_uploader(
        "Upload Passport Photograph", type=["jpg", "jpeg", "png"])

    # OPEN PASSPORT PHOTOGRAPH
    if passport_photograph:
        original_size = get_file_size(passport_photograph.getvalue())
        passport_img = Image.open(passport_photograph)

        # DETAILS OF ORIGINAL PASSPORT
        with st.container(border=True):
            st.title("Original Passport Photograph")
            col1, col2 = st.columns([1.5, 1])

            with col1:

                st.image(
                    passport_img,
                    use_container_width=True
                )

            with col2:

                st.metric(
                    "Dimensions",
                    f"{passport_img.width} × {passport_img.height}"
                )

                st.metric(
                    "File Size",
                    original_size
                )

                st.metric(
                    "Format",
                    f"{passport_img.format}"
                )
        if passport_img.mode in ("RGBA", "LA", "P"):
            passport_img = passport_img.convert("RGB")

        passport_img.thumbnail(PASSPORT_SIZE)

        # CONVERT PIL IMAGE TO BYTES FOR DOWNLOAD
        buf = io.BytesIO()
        passport_img.save(buf, format="JPEG", quality=90)
        byte_im = buf.getvalue()

        # TRANSFORMATION
        transformed_bytes = buf.getvalue()

        transformed_size = get_file_size(
            transformed_bytes)

        st.success("Passport Photograph transformed Successfully")

        # DETAILS OF TRANSFORMED PASSPORT
        with st.container(border=True):
            st.title("Transformed Passport Photograph")
            col1, col2 = st.columns([1.5, 1])

            with col1:

                st.image(
                    passport_img,
                    use_container_width=True
                )

            with col2:

                st.metric(
                    "Dimensions",
                    f"{passport_img.width} × {passport_img.height}"
                )

                st.metric(
                    "File Size",
                    transformed_size
                )

                st.metric(
                    "Format",
                    "JPG"
                )

        # DOWNLOAD RESIZED PASSPORT
        st.download_button(
            file_name="Resized_photo.jpg",
            data=byte_im,
            label="⬇️Download Resized Photo",
            mime="image/jpg"
        )
