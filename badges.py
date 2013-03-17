"""
Prints badges from an Eventbrite attendee CSV file.
Configuration file is config-badge.py
Prints two of each badge alongside to make double-sided badge production easier.

ReportLab works with two separate components.  The canvas component sets up document
template.  This includes graphics, page geometry, and "frames" (object containers).
The platypus component can handle "flows" (data streams), populating the frames.

The idea is that you can set up a frame as a "catcher's mitt".  When data
is thrown at it, platypus is clever enough to populate the frames, moving onto
the next one when the current one fills up, moving the next page when the current
one fills up, etc.

The best case scenario is a single docuent template that accommodates all the data.
In a less-than-perfect world, the data needs to be separated then run against a
canvas well-suited for it.

Here, we'll try to design a canvas sufficiently generic that it can be used for all
the permutations of the badges we can think of.  There are a couple of potential issues 
(or maybe opportunities):  the elements overwrite one another (last declared wins); 
since platypus tries to fill all the elements, we need placeholders for sparse
entries.

An alternative would to be to manually handle platypus' functions - not so bad here because
all we need to track is badges/sheet and page breaks.  The drawback is that we'd have a 
multi-page canvas that could get huge for large data sets.

drawImage works from the lower, left corner (the x,y)
"""
##TODO:  why isn't exhibitor a ticket type?
exhibitor = False

#
# Certain simplifying assumptions are made. We assume
# 1. That the same email is always associated with the same name
# 2. That there will be no more ticket types needing identification
#    than blob graphics.
# 3. The badges are the 3" x 4" six-up, such as Avery 5392.
# 4. That everything will always be happily US letter-sized.
# 5. That the local filestore has data and image files present.
#

##TODO:  test special events
##TODO:  test completeness of inputs
##TODO: make framing an option
##TODO:  test "y" specifications
##TODO:  test decimal position specs
from collections import defaultdict
import reportlab
from reportlab.platypus import (PageTemplate, BaseDocTemplate, Paragraph, 
                                Table, TableStyle, Spacer, Frame, FrameBreak)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth 
from reportlab.lib import colors

import PIL.Image

#from ticketspecs import specialtickets, ims, bastion, feather
from badge_utils import blanks, generate_blobs

from config_reader import confReader
from badge_utils import register_fonts, convert_units, convert_paragraph_style, build_ticket, getxy


#grab the raw specifications from the spec sheet
reader = confReader()
config =reader.readFile()

#apply tweaks to make the specs play well with reportLab

#register the fonts, adjust the config if necessary to adjust for duplicates
config = register_fonts(config)
#add the unit specifications to the label and paper dimensions
config = convert_units(config)
#convert user paragraph format specs to reportLab objects
config = convert_paragraph_style(config)

#create color blobs (to mark special tickets
#config = generate_blobs(config)
#blobs = [colorblobs[t.type] for t in tix if t.type in colorblobs] 


#Add label geometry to namespace (mostly for readability)
page_horiz_margin = config['media_specs']['page_horiz_margin']
page_vert_margin = config['media_specs']['page_vert_margin']
page_horizontal_gap = config['media_specs']['page_horiz_gap']
page_vertical_gap = config['media_specs']['page_vert_gap']
page_width = config['media_specs']['page_width']
page_height = config['media_specs']['page_height']
#
lab_width =config['media_specs']['label_width']
lab_height=  config['media_specs']['label_height']
lab_horizontal_margin = config['media_specs']['label_horiz_margin'] 
lab_vertical_margin = config['media_specs']['label_vert_margin'] 
                        
#figure out rows/colums of labels based on effective height/width
eff_page_width = page_width - 2 * page_horiz_margin #assumes r/l margins same
eff_label_width = lab_width + page_horizontal_gap
label_cols = int(eff_page_width / eff_label_width)
#
eff_page_height = page_height - 2 * page_vert_margin
eff_lab_height = lab_height + page_vertical_gap 
label_rows = int(eff_page_height / eff_lab_height)

#horizontal and vertial starting points                     
XS = tuple(page_horiz_margin+x*eff_label_width for x in range(0,label_cols))
YS = tuple(page_vert_margin+x*eff_lab_height for x in range(0,label_rows))           
#


#misc parameters from the spec sheet
#
#determine if the labels are preprinted
preprinted = config['preprinted']

##TODO:  make this more generic (de-feather it)
#feather = PIL.Image.open("images/feather.png")
#scaling = 75.0/feather.size[0]
#feather = feather.resize(tuple(int(scaling*x) for x in feather.size))
#fw, fh = feather.size


class localDocTemplate(BaseDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        ##TODO:        """Couldn 't we just inherit __int__?"""
        BaseDocTemplate.__init__(self, *args, **kwargs)

def pageBackground(canvas, doc):  

    """Called at the start of processing for each page.
    This is where we decorate each badge with images or
    whatever else is required."""
    if preprinted:
        return

    canvas.saveState()  #save current state of canvas
    canvas.resetTransforms()  #resets origin to (0,0)
    
    #set elements in common for all badges

    for y in YS:
        for x in XS:
            ##grab a delegate from the delebate file
            for i in config['common_images']:
                img_name, img_loc = i
                img_file, img_height, img_width = config['image'][img_name]
                label_x, label_y = getxy(img_name, img_loc, config)               
                canvas.drawImage( img_file, x + label_x, y + label_y , width = img_width, 
                                  height = img_height, preserveAspectRatio = True) 
    canvas.restoreState()


class Ticket:
    def __init__(self, first, last, email, twitter, typ):
        self.first = first
        self.last = last
        self.email = email
        self.twitter = twitter
        self.type = typ
        
#reads the delegates file
delegates = config['delegates']

#build list of tickets sorted by last, first
tickets = defaultdict(lambda : [])
for line in delegates:
    ticket = Ticket(*line)
    tickets[ticket.email].append(ticket)    
tickets = tickets.items()
tickets.sort(key=lambda t: (t[1][0].first.upper(), t[1][0].last.upper()))    

#Create the "frames" that will hold document elements
frames = []
for y in YS:
    for x in XS:
        frames.append(Frame(x, y, lab_width, lab_height, showBoundary=1))   
        
#create the page template - general specs for the entire sheet
pt = PageTemplate(frames=frames, 
                  pagesize=(page_width, page_height ), 
                  onPage=pageBackground,)

# Create the Document template - note that frames are absolutely
# positioned on the page, NOT relative to the margins

dt = localDocTemplate("badges.pdf", showBoundary=True, pageTemplates=[pt],
                      leftMargin=0.0, rightMargin=0.0,topMargin=0.0, 
                      bottomMargin=0.0)

story = []

for email, tix in tickets:
    ##TODO:  maybe make array of blobs, so one badge/participant?
    ##TODO:  check for duplicates, multilpe reg. w/ one email?
         
    #build each ticket based on the "recipe" in the config     
    main_elements = config['badge_layout']
    if tix[0].type in config['special_ticket']:
        special_ticket_elements = config['special_ticket'][tix[0].type]  #standard, special, etc.
    else:
        special_ticket_elements=[]
   
    story = story + build_ticket(tix, config, main_elements, special_ticket_elements)
    
for s in story:
    print s
    print '****'

dt.build(story)    

    
