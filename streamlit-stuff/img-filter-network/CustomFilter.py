from PIL import Image
import numpy as np
from network_dispatcher.dispatcher import *
import inspect

class Filter():
    """
    Custom Filter class for PIL images. 
    example: 
    ```
    def my_filter(r,g,b):
        return r,g,b
    
    filter = Filter("my_filter", my_filter)
    new_image = filter.apply(image)
    ```
    
    """
    def __init__(self, name, filter):
        self.name = name
        self.filter_function = filter

    def get_channels(self, image):
        red = np.asarray(image, dtype=np.float)[:,:,0]
        green = np.asarray(image, dtype=np.float)[:,:,1]
        blue = np.asarray(image, dtype=np.float)[:,:,2]
        return red, green, blue
        
    def apply(self, image, dispatch_Network, dispatcher:Dispatcher,needsMore,  args):
        r,g,b  = self.get_channels(image)
        if dispatch_Network:
            
            r,g,b = dispatcher.dispatch(inspect.getsource(self.filter_function),  r,g,b, image, needsMore, args)
        else:
            r,g,b = self.filter_function(r,g,b, args)
        # r,g,b = self.smooth(r,g,b)
        
        r = np.asarray(r, dtype=np.uint8)
        g = np.asarray(g, dtype=np.uint8)
        b = np.asarray(b, dtype=np.uint8)
        r = Image.fromarray(r)
        g = Image.fromarray(g)
        b = Image.fromarray(b)
        
        # convert back to image
        new_image = Image.merge("RGB", (r, g, b))
        return new_image

