
import streamlit as st
from PIL import Image
from PIL import ImageFilter
from CustomFilter import Filter
from datetime import datetime
from network_dispatcher.dispatcher import Dispatcher
from filters import timeso5, savgolfilter, medianfilter
st.set_page_config(layout="wide")
sl = False
st.write("""
    # Filter images
""")
global dispatcher
if 'dispatcher' in st.session_state:
    dispatcher = st.session_state["dispatcher"]
st.write("""
This script is still in early development as part of a school-project.
Everything is subject to change and the structure is not well thought out yet.

Please use quite small images for now, as the script is not optimized for large images yet.

If you intend to open more images, please either restart the script or press "Clear Cache" before loading a new image.

If you want to use the script on your own computer, you can find the source code on [GitHub](
    https://github.com/Timster275/streamlit-projects/ "GitHub"
    ).

""")
if st.button(" Init Network "):
    dispatcher = Dispatcher("0.0.0.0", 2405)
    st.session_state["dispatcher"] = dispatcher

global curr_image
global main
if 'curr' in st.session_state:
    curr_image = st.session_state['curr']
else:
    curr_image = None
file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if file is not None:
    st.session_state['original'] = file
    main_col, action_col, action_col1= st.columns([2,1,1])
    with main_col:
        if not curr_image==None:
            main = st.image(curr_image, caption="Uploaded Image.", use_column_width=True)
        else:
            main = st.image(file, caption="Uploaded Image.", use_column_width=True)
            curr_image = Image.open(file).convert("RGB")

    
    
    def fill_main_image(image, ):
        global main
        main.image(image)
        st.session_state['curr'] = image
        st.session_state['prev_name'] = file.name
        st.experimental_rerun()
        #return image

    def show_channels(image):
        red, green, blue = image.split()
        new_green = green.point(lambda i: i * 0)
        new_blue = blue.point(lambda i: i * 0)
        new_red = red.point(lambda i: i * 0)
        # convert back to image
        red_image = Image.merge("RGB", (red, new_green, new_blue))
        green_image = Image.merge("RGB", (new_red,green, new_blue))
        blue_image = Image.merge("RGB", (new_red, new_green, blue))
        st.session_state['red'] = red_image
        st.session_state['green'] = green_image
        st.session_state['blue'] = blue_image
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Red")
            st.image(red_image, caption="Red channel.", use_column_width=True)
            if st.button("Show Red"):
                fill_main_image(red_image)
        with col2:
            st.write("Green")
            st.image(green_image, caption="Green channel.", use_column_width=True)
            if st.button("Show Green"):
                fill_main_image(green_image)

        with col3:
            st.write("Blue")
            st.image(blue_image, caption="Blue channel.", use_column_width=True)
            if st.button("Show Blue"):
                fill_main_image(blue_image)
        colrg, colrb, colbg = st.columns(3)
        with colrg:
            st.write("Red-Green")
            rg = Image.merge("RGB",(red,green, new_blue))
            st.image(rg)
        with colrb:
            st.write("Red-Blue")
            rb = Image.merge("RGB",(red,new_green, blue))
            st.image(rb)
        with colbg:
            st.write("Blue-Green")
            bg = Image.merge("RGB", (new_red, green, blue))
            st.image(bg)
        return red_image, green_image, blue_image

    if st.button('Original'):
        fill_main_image(Image.open(st.session_state['original']).convert("RGB"))
    if st.button('Clear chache'):
        st.session_state.clear()
    red_image, green_image, blue_image = show_channels(curr_image)
    
    
    with action_col:
        xval = st.slider(
            "xmedian", 1, 31, 1, step=1, key="xmedian",
        )
        yval = st.slider(
            "ymedian", 1, 31, 1, step=1, key="ymedian", 
        )

        if st.button("Median"):
            flt = Filter('median', medianfilter)
            img = flt.apply(curr_image,False,dispatcher, [int(xval), int(yval)])
            curr_image = fill_main_image(img)
        
    with action_col1:
        if st.button("Times Filter"):
            flt = Filter('times', timeso5)
            img = flt.apply(curr_image,True,dispatcher, 5)
            curr_image = fill_main_image(img)
