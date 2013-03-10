# coding: utf-8      

'''this script comes from https://code.google.com/p/elaphe/ and is designed
to test whether ghostscript is installed and accessible.  Upon execution, 
it creates an image file with text called foo.png'''

from StringIO import StringIO
from PIL.EpsImagePlugin import EpsImageFile

src = """%!PS-Adobe 2.0                                                         
%%BoundingBox: 0 0 144 144                                                      
36 36 72 72 rectfill                                                            
/Courier findfont 12 scalefont setfont                                          
36 120 moveto (text) show                                                       
showpage                                                                        
"""

im = EpsImageFile(StringIO(src))
im.save('foo.png')
x=1