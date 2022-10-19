from turtle import onclick
import streamlit as st
import numpy as np
from PIL import Image
from scipy.signal import savgol_filter
from PIL import ImageFilter
from CustomFilter import Filter
from filters import timeso5, savgolfilter
st.set_page_config(layout="wide")
sl = False
st.write("""
    # Filter images:
""")

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
        st.write("Apply filter:")
        if st.button("Blur"):
            img = curr_image.filter(ImageFilter.BLUR)
            curr_image = fill_main_image(img)
        if st.button("Contour"):
            img = curr_image.filter(ImageFilter.CONTOUR)
            curr_image = fill_main_image(img)

        if st.button("Detail"):
            img = curr_image.filter(ImageFilter.DETAIL)
            curr_image = fill_main_image(img)
        if st.button("Edge Enhance"):
            img = curr_image.filter(ImageFilter.EDGE_ENHANCE)
            curr_image = fill_main_image(img)
        if st.button("Edge Enhance More"):
            img = curr_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            curr_image = fill_main_image(img)
        if st.button("Emboss"):
            img = curr_image.filter(ImageFilter.EMBOSS)
            curr_image = fill_main_image(img)
        
    with action_col1:
       
        if st.button("Find Edges"):
            img = curr_image.filter(ImageFilter.FIND_EDGES)
            curr_image = fill_main_image(img)
        if st.button("Smooth"):
            img = curr_image.filter(ImageFilter.SMOOTH)
            curr_image = fill_main_image(img)
        if st.button("Smooth More"):
            img = curr_image.filter(ImageFilter.SMOOTH_MORE)
            curr_image = fill_main_image(img)
        if st.button("Sharpen"):
            img = curr_image.filter(ImageFilter.SHARPEN)
            curr_image = fill_main_image(img)
        if st.button("Unsharp Mask"):
            img = curr_image.filter(ImageFilter.UnsharpMask)
            curr_image = fill_main_image(img)
        tvalue = st.slider("Dim %", 0,100,50)
        if st.button("Dim"):
            flt = Filter("custom", timeso5)
            img = flt.apply(curr_image, {"times": int(tvalue)/100})
            curr_image = fill_main_image(img)
        def set_sl():
            sl = True
        svalue = st.slider(
            "Savgol_Strength", 0.0, 100.0, 1.0, step=1.0, key="savgol", on_change=set_sl
        )
        if st.button("Savgol"):
            flt = Filter("Savgol", savgolfilter)
            img = flt.apply(curr_image, {"window_length": svalue, "polyorder": 3})
            curr_image = fill_main_image(img)
        

        

    # red, green and blue all contain a 2dim array with the pixel values of their channels
    