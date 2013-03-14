'''Routine for reading the config file.  Returns a dict of all user settings'''
from inspect import isgenerator
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics

import config_badge as cb
import badge_utils as utils

config = {}

class confReader():
    def __init__(self):
        pass
    
    def readFile(self):   
        #Read delegates.
        if "custom_file" in cb.delegates_file:
            delegates = utils.csv_reader(cb.delegates_file[0], 
                                         cb.delegates_file[1])
        if "eventbright_file" in cb.delegates_file:
            delegates = utils.evb_reader(cb.delegates_file[0],
                                         cb.delegates_file[2],
                                         cb.delegates_file[1])
        if "internet_file" in cb.delegates_file:
            ##TODO: implement reading directly from eventbright
            delegates = None
            
        assert isgenerator(delegates)   #our data acquaition logic failed if this isn't the case
        
        config.update({'delegates': delegates})
        
        #units
        if cb.units == "inches":
            config.update({'units': inch})
        else:
            config.update({'units': mm})
         
        #badge media specs
        tmp = {}
        tmp.update({'label_width' : cb.label_width})
        tmp.update({'label_height' : cb.label_height})
        tmp.update({'label_left_margin' : cb.hm})
        tmp.update({'label_top_margin' : cb.vm})
        tmp.update({'page_left_margin' : cb.LM})
        tmp.update({'page_horiz_gap' : cb.XM})
        tmp.update({'page_top_margin' : cb.TM})
        tmp.update({'page_vert_gap' : cb.YM})
        tmp.update({'page_height' : cb.page_height})
        tmp.update({'page_width' : cb.page_width})   
        config.update({"media_specs":tmp})
                            
        #locations within the badge for image placement
        config.update({"location": dict(cb.location)})
               
        #image files
        config.update({'image': dict(cb.image)})
        
        #fonts
        config.update({'font': dict(cb.font)})
        
        #paragraph styles and fonts
        config.update({'paragraph_style': dict(cb.paragraph_style)})
        
        #text field formats
        config.update({'text_field_format': dict(cb.font)})  
        
        #basic badge layouts
        config.update({"location": dict(cb.badge_layout)})      
        
        #tweaks for individual special ticket types
        config.update({"special_ticket": dict(cb.special_ticket)})         

        #labels preprinted
        config.update({"preprinted": cb.labels_preprintd})
        
        return config

if __name__=="__main__":
    reader = confReader()
    conf = reader.readFile()
    pass
