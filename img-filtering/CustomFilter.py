
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
        red = np.asarray(image, dtype=np.float)[:,:,0]
        print(red[0][0])
        green = np.asarray(image, dtype=np.float)[:,:,1]
        blue = np.asarray(image, dtype=np.float)[:,:,2]
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

    def wrapper(self,function, r,g,b, num, args, queue):
        r,g,b = function(r,g,b,args)
        print("one done")
        queue.put(r,g,b,num)

    def apply(self, image, args):
        r,g,b  = self.get_channels(image)
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

