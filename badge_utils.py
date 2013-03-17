from __future__ import division
##TODO:  Images are not getting scaled.  this makes them too (tall/wide) to fit on the frame.

'''
reportlab.platypus.doctemplate.LayoutError: Flowable <Image at 0x950b56c 
filename=./images/blob_black.png>(360.0 x 360.0) 
too large on page 1 in frame None(276.0 x 204.0*) of template None

'''

"""
badge_utils.py: utility functions for badge printer input
"""

import codecs
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Image
from reportlab.platypus import (PageTemplate, BaseDocTemplate, Paragraph, 
                                Table, TableStyle, Spacer, Frame, FrameBreak)

from PIL import Image as PILImage

def fsplit(line, N):
    """Parse a line from a CSV file and return the fields it contains
       ensuring that the whole line is consumed or raising an AssertionError exception."""
    pos = 0
    fields = []
    for _ in range(N):
        if line[pos] == '"':
            start = pos
            end = line.find('"', pos+1)
            while end+1<len(line) and line[end+1] == '"':
                pos = end+1
                end = line.find('"', pos+1)
            field = line[start+1:end].replace('""', '"')
            pos = end+2
        else:
            end = line.find(',', pos)
            field = line[pos:end]
            pos = end+1
        fields.append(field)
    if len(line) != pos:
        print("***", line)
        print("Pos:", pos, "Remaining:", line[pos:])
    assert abs(pos -len(line)) <=1 # sanity check
    #assert pos == len(line) # a bit too strict w/trailing /r/n, etc characters
    return fields

def evb_reader(filename, fields, encoding):
    """Yields sucessive data sets from an Eventbrite delegate summary."""
    f = codecs.open(filename, "r", encoding)
    for line in f:
        cols=fsplit(line, 27)
        yield tuple(cols[n] for n in fields)

def csv_reader(filename, encoding):
    """Yields successive data sets from a CSV file."""
    f = codecs.open(filename, "Ur", encoding)
    for line in f:
        if line.startswith("#"):
            continue
        cols = line[:-1].split(",")
        #yield tuple(cols+["manual"])  
        #Do we really care that this is manual? If so Ticket must accept this arg.
        yield tuple(cols)  
def blanks(N):
    """Yields blank tickets to allow blank labels to be printed."""
    for i in range(N):
        yield ("", "", "", "", "")
        
def register_fonts(config):
    '''
    This routine registers all the fonts specified in the config_badge routine.  Since 
    PDFDocument::pdfdoc breaks (during build) when the same font is registered more than
    once, we'll prevent that here.  When we're done, all the unique fonts will be registred and
    the config dictionary will be augmented with a dictionary to handle mapping between font names
    specified and the ones really registered.
    '''
    

    fonts = config['font']
    registered = {}
    update_list = []
    

    for fname, ffile  in fonts.iteritems():
        #is this font file already registered?
        if not ffile in registered.values():         
            try:  #if we haven't registered it, do so and add to registered dict
                pdfmetrics.registerFont(TTFont(fname, ffile))
                registered.update({fname:ffile})
            except:
                print "Sorry, I couldn't find font file '%s'" %ffile
                raise
        else:  #otherwise, we need to know what the associated font name is
            for k, v in registered.iteritems():
                #and map the user's (duplicate) font name to the one already registered
                if ffile == v:
                    update_list.append((fname, k))  #(user provided name, registered name)
        
    #apply the updates to the paragraph style section of the config dict
    pending_updates = dict(update_list)             
    pstyles = config['paragraph_style']
    for p_name, p_font_spec in pstyles.iteritems():
        font_name = p_font_spec[0]  
        #does this style have a font that's one of our duplicates?
        if font_name in pending_updates:
            #if so, we'll update the dict element by creating a new tuple, 
            #  replacing the name of the font only
            pstyles.update( {p_name: (pending_updates[font_name], 
                                      p_font_spec[1], 
                                      p_font_spec[2],
                                      p_font_spec[3],
                                      p_font_spec[4],
                                      p_font_spec[5],
                                     )})
        
    #update the config dict with the new paragraph element
    config['paragraph_style'].update(pstyles)
    return config
    
def convert_units(config):
    '''
    Converts user-specified units to the paper/label dimensions. The "units"
    come from reportlab.lib.units (added to the config dict with configReader::confReader).
    
    This makes the mainline code a bit more flexible and easy to read.
    '''
    media = config['media_specs']  #note this a "live" copy of config; 
    image= config['image']
    units = config['units']

    #important note to self.  You CANT simply iterate thru a dict an update it.  The deck can get reshuffled with
    #   every update - doubling up on some and leaving others out (potentially)
    
    #this takes care of units in the media specifications
    pending_updates =[]
    #this takes care of units in the media specifications
    for spec, value in media.iteritems():    
        pending_updates.append((spec, value*units)) 
    for p in pending_updates:
        media.update({p[0]:p[1]})

    pending_updates =[]
    #this takes care of units in the image specifications
    for k,v in image.iteritems():    
        #k is image name, 
        fname, height, width = v
        pending_updates.append((k, (fname, height *units, width * units) )) 
    for p in pending_updates:
        image.update({p[0]:p[1]})
        
    #no need to update config, as media is a "live" copy of one of its elements
    return config
        
def convert_paragraph_style(config):
    #converts user input into a reportLab ParagraphStyle object and updates config
    convert = {'center': TA_CENTER, 'right': TA_RIGHT, 'left': TA_LEFT}
    updates_pending = []
    for style in config['paragraph_style'].iteritems():
        k, v = style
        #convert justification into reportLab constants
        if v[1] in convert:
            justify = convert[v[1]]
        else:
            print "Warn:  From badge_config.py, couldn't understand %s" %k
            print "Justification needs to be 'right', 'left', or 'center'."
            print "centering text." 
            justify = convert['center']
        ps = ParagraphStyle(k, fontName = v[0], fontSize = v[2], leading = v[3],
                            alignment = justify, 
                            spaceBefore = v[4], spaceAfter = v[5])
        updates_pending.append((k,ps))  #append({k.ps} ) appends an object of type 'set' ?!
    
    #update config
    
    for u in updates_pending:
        config['paragraph_style'].update({u[0]:u[1]})
    return config

def generate_blobs(config):
    #may generate color blobs someday
    return config

def getxy(image_name, loc, config):
    '''Calculates the lower left position based on the image definition 
    and a user-friendly location identification from the spec sheet.  
    
    For convenience, we've allowed the user to specify image locations in
    terms of 'center', 'right', etc.  Reportlab thinks of image locations
    in terms of the absolute (x,y) coordinates relative to the bottom,
    left of the container object.
    
    Here, we translate.
    ##TODO:  scale images
    '''
    image_height = config['image'][image_name][1]
    image_width = config['image'][image_name][2]
    label_height = config['media_specs']['label_height']
    label_width = config['media_specs']['label_width']
    vert_margin = config['media_specs']['label_vert_margin']
    horiz_margin = config['media_specs']['label_horiz_margin']
    
    #grab the image location (specified in % of printable area)
    xpct, ypct = config['location'][loc]
    
    print image_name
    #y-coordinate stated in terms of position of bottom of element 
    if ypct in [0, 50, 100]:  #special values
        if ypct == 100:  #bottom
            y = vert_margin 
        elif ypct == 50:  #vertically centered
            y = .5 * label_height - .5 * image_height
        elif ypct == 0:  # top
            #y = label_height - 2 *vert_margin - image_height
            y = label_height -  vert_margin - image_height
    else:
        y = (label_height -  vert_margin) * (100 - ypct)/100
            
    #x-coordinate stated in terms of position of left of element
    if xpct in [0, 50, 100]:  #special values   
        if xpct == 0:  #left
            x = horiz_margin
        elif xpct == 50:  #horizontally centered
            x = .5 * label_width - .5 * image_width
        elif xpct == 100:  #right
            x = label_width - image_width - horiz_margin
    else:  #no special values
        x = (label_width - 2 * horiz_margin) * (100 - xpct)/100
    
    return (x,y)    

def fix_twitter(twit):
    #if twitter handle doesn't come with a "@" add it
    if len(twit) > 0:
        if twit[0].strip() == '@':
            pass
        else: twit = '@' + twit
    return twit

 
def build_ticket(tix, config, main_elements, special_ticket_elements):
    
    '''
    Combine the user's general badge specifications with any pertenant
    to this ticket's special status (if applicable).  Then build a 
    recipe ("story") using platypus objects.  This will serve as a
    "flowable" stream of information to populate the individual badges.
    '''
    #make a dict so we can map text_field names (user provided) to 
    #  ticket objects
    tix_dict = {'first_name':tix[0].first, 
                'last_name':tix[0].last,
               'email':tix[0].email, 
               'twitter_handle':fix_twitter(tix[0].twitter.strip()) }
    
    badge = main_elements
    #knit in special elements (recursive so special elements can refer to each other)
    for e in special_ticket_elements:
        insert_after = e[len(e)-1]  #this is the tag after which we'll insert this element
        tmp =[]
        for b in badge:
            tmp.append(b)
            if b[0]==insert_after:
                tmp.append(e)
        badge = tmp[:]
                
     #we have our badge elements - so convert to platypus-friendly format
    story = []
    for b in badge:
        elem = b[1]
        #image file
        if elem in config['image']:
            fn, w, h = config['image'][elem]
            raw_image= PILImage.open(fn) #this is a PIL Image object
            new_image = raw_image.resize((int(w), int(h)))           
            #story.append( Image(new_image) )
            story.append(Image(fn, w, h))
            
        #text field 
        elif elem in config['text_field']:         
            #in case we have a null field value (no email, maybe) print a whitespace
            #  this should force appropriate vertical spacing
            if len(tix_dict[elem]) == 0:
                text = " "
            else:
                text = tix_dict[elem]
            p_style_name = config['text_field'][elem]
            p_style = config['paragraph_style'][p_style_name]
            story.append(Paragraph(text,           #value
                                   p_style         #platypus ParagraphStyle 
                                    ))        
            
        elif elem[0:6]=='spacer':
            space_pct= int(elem[6:])/100
            space_height = (config['media_specs']['label_height'] - 
                            2 * config['media_specs']['label_vert_margin']) * space_pct
            space_width = 1
            #width is an arbitrary placeholder - should be OK, but...
            story.append(Spacer(space_height, space_width))
            
        elif elem in ['null', 'end_tag']:  #these are just flags in the config file
            pass
            
        else:  #if it's not an image, text_field, or spacer, we'll call it text
            p_style = config['paragraph_style'][b[2]]
            story.append(Paragraph(str(elem),         #text 
                                   p_style) )         #a platypus ParagraghStyle
    
    story.append(FrameBreak())  #this completes the badge

    #concantenate two copies if we're doing double-sided badges
    if config['double_badges']:
        return story + story
    else:
        return story


 