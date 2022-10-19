from PIL import Image
import numpy as np

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
        red = np.asarray(image)[:,:,0]
        green = np.asarray(image)[:,:,1]
        blue = np.asarray(image)[:,:,2]
        return red, green, blue

    def smooth(self, r,g,b):
        for i in range(0, len(r)-1):
            for j in range(0, len(r[i])-1):
                if r[i][j] > 255:
                    r[i][j] = 255
                if g[i][j] > 255:
                    b[i][j] = 255
                if b[i][j] > 255:
                    b[i][j] = 255
        return r,g,b

    def apply(self, image, args):
        r,g,b  = self.get_channels(image)
        r,g,b = self.filter_function(r,g,b, args)
        # r,g,b = self.smooth(r,g,b)
        
        r = r.astype(np.uint8)
        g = g.astype(np.uint8)
        b = b.astype(np.uint8)
        r = Image.fromarray(r)
        g = Image.fromarray(g)
        b = Image.fromarray(b)
        
        # convert back to image
        new_image = Image.merge("RGB", (r, g, b))
        return new_image

