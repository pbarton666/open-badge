"""
Prints badges from an Eventbrite attendee CSV file.
Configuration file is config-badge.py
Prints two of each badge alongside to make double-sided badge production easier.
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

import PIL.Image

from ticketspecs import specialtickets, ims, bastion, feather
from badge_utils import blanks, generate_blobs#, read_delegate_file

from config_reader import confReader
from badge_utils import register_fonts, add_units, convert_paragraph_style

#grab the raw specifications from the spec sheet
reader = confReader()
config =reader.readFile()

#apply tweaks to make the specs play well with reportLab

#register the fonts, adjust the config if necessary to adjust for duplicates
config = register_fonts(config)
#add the unit specifications to the label and paper dimensions
config = add_units(config)
#convert user paragraph format specs to reportLab objects
config = convert_paragraph_style(config)
#create color blobs (to mark special tickets
#config = generate_blobs(config)
#blobs = [colorblobs[t.type] for t in tix if t.type in colorblobs] 


#Add label geometry to namespace (mostly for readability)
page_left_margin = config['media_specs']['page_left_margin']
page_top_margin = config['media_specs']['page_top_margin']
page_horizontal_gap = config['media_specs']['page_horiz_gap']
page_vertical_gap = config['media_specs']['page_vert_gap']
page_width = config['media_specs']['page_width']
page_height = config['media_specs']['page_height']
#
lab_width =config['media_specs']['label_width']
lab_height=  config['media_specs']['label_height']
lab_horizontal_margin = config['media_specs']['label_left_margin'] 
lab_vertical_margin = config['media_specs']['label_top_margin'] 
                        
#figure out rows/colums of labels based on effective height/width
eff_page_width = page_width - 2 * page_left_margin #assumes r/l margins same
eff_label_width = lab_width + page_horizontal_gap
label_cols = int(eff_page_width / eff_label_width)
#
eff_page_height = page_height - 2 * page_top_margin
eff_lab_height = lab_height + page_vertical_gap 
label_rows = int(eff_page_height / eff_lab_height)

#horizontal and vertial starting points                     
XS = tuple(page_left_margin+x*eff_label_width for x in range(0,label_cols))
YS = tuple(page_top_margin+x*eff_lab_height for x in range(0,label_rows))           
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
        """Couldn 't we just inherit __int__?"""
        BaseDocTemplate.__init__(self, *args, **kwargs)

def pageBackground(canvas, doc):  

    """Called at the start of processing for each page.
    This is where we decorate each badge with images or
    whatever else is required."""
    if preprinted:
        return
    # saveState keeps a snapshot of the canvas state, so you don't
    # mess up any rendering that platypus will do later.
    canvas.saveState()
    canvas.resetTransforms()
    # Reset the origin to (0, 0), remember, we can restore the
    # state of the canvas later, so platypus should be unaffected.
    for y in YS:
        for x in XS:
            ##grab a delegate from the delebate file
    
            
            canvas.drawImage("images/bastion.png",
                    x+(label_width/2.0)-inch, y+(label_height/2.0)-inch,
                    width=2*inch, height=2*inch, preserveAspectRatio=True)
            # canvas.drawImage("images/feather.png",
            #         x, y,
            #         width=0.5*inch, preserveAspectRatio=True)
            for x1 in (lab_horizontal_margin, label_width-lab_horizontal_margin):
                for y1 in (lab_vertical_margin, label_height-lab_vertical_margin):
                    canvas.drawImage("images/feather.png",
                        x+x1-fw/2, y+y1-fh/2, width=fw, height=fh,
                        preserveAspectRatio=True)
            if exhibitor:
                ##TODO: move to a config file
                canvas.setFont("bannerFont", 18)
                for y1 in (lab_vertical_margin, label_height-lab_vertical_margin):
                    twidth = stringWidth("EXHBITOR", "bannerFont", 18)
                    canvas.drawCentredString(x+label_width/2, y+y1-6, "EXHIBITOR")
    # Finally, restore the canvas back to the way it was.
    canvas.restoreState()
#
# If the following assertion fails you need more images
#
##don't need this if specs are separate
assert len(specialtickets) <= len(ims)
colorblobs = dict(zip(specialtickets, ims))
class Ticket:
    def __init__(self, first, last, email, twitter, typ):
        self.first = first
        self.last = last
        self.email = email
        self.twitter = twitter
        self.type = typ
        self.fonts = {}

##TODO:  make a rule about collissions e.g., when adding different logos for multiple tutorial sessions        
##TODO:  for testing, print example of each badge type specified w/ fake information

#
# Build a list of tickets held by each email address
#
tickets = defaultdict(lambda : [])
fields = (3, 2, 4, 19, 6)
#delegates = evb_reader("Attendees-3952423806.csv", fields, "utf-8")
#delegates = evb_reader("Attendees-20130225.0247.csv", fields, "utf-8")
#delegates = blanks(6)

#reads the delegates file
delegates = config['delegates']
for line in delegates:
    ticket = Ticket(*line)
    tickets[ticket.email].append(ticket)
    
#sort them (this is by first_name, last_name)    
tickets = tickets.items()
tickets.sort(key=lambda t: (t[1][0].first.upper(), t[1][0].last.upper()))    

#Create the "frames" that will hold document elements
frames = []
for y in YS:
    for x in XS:
        frames.append(Frame(x, y, lab_width, lab_height))
        
#create the page template - general specs for the entire sheet
pt = PageTemplate(frames=frames, 
                  pagesize=(page_width, page_height ), 
                  onPage=pageBackground,)
#
# Create the Document template - note that frames are absolutely
# positioned on the page, NOT relative to the margins
#
dt = localDocTemplate("badges.pdf",
                      showBoundary=False,
                      pageTemplates=[pt],
                      leftMargin=0.0, 
                      rightMargin=0.0, 
                      topMargin=0.0, 
                      bottomMargin=0.0)

#Now, build a list that will serve to hold the label elements, 
#  here called a "story"

story = []

for email, tix in tickets:
    print tix[0].first  ###this is a debugging statement only
    ##TODO:  what if an admin registered three people?  would they all get the same blobs?
    ##TODO:  what if the same person registered twice, once for a tutorial?
    ##TODO:  why not loop thru all the same (email, first) and consolidate ticket types?
    #this builds an array of images, each representing a special ticket
    blobs = [colorblobs[t.type] for t in tix if t.type in colorblobs]  #these are mini-logos for each tutorial
    #non_blob_tix = sum(t.type not in colorblobs for t in tix)
    #if non_blob_tix != 1:
    #    print email,  non_blob_tix
    t = tix[0].twitter.strip()
    for _ in "front", "back":
        # MORE ACCURATE, AND AUTOMATED, HEIGHT CALCULATIONS REQUIRED
        # TO ALLOW GENERAL VERTICAL CENTERING OF ARBITRARY LAYOUTS
        if not t:  #no twitter handle provided
            story.append(Spacer(inch*3, inch/8.0))  ###a spacer object from reportLab.platypus
        if not blobs:
            story.append(Spacer(inch*3, inch/5.0))
        #apply styles to the text bits (fsty is the style for the first name, etc.)
        story.append(Paragraph(tix[0].first, fsty))  ###these are the paragraph formats
        story.append(Paragraph(tix[0].last, lsty))
        story.append(Paragraph(tix[0].email, esty))
        if t:
            story.append(Paragraph("@"+t, tsty))
        if blobs:
            story.append(Table([blobs]))  ###this is just a table of the mini-logos
        story.append(FrameBreak())
#
# Having created the story (i.e., a label), we flow it through the pages i.e., 
#  build the pdf document with  pdfdoc.py (part of PDFDocument package)
#debug
for s in story:
    print s
    print "***************"    
dt.build(story)  ###looks like pdfdoc has logic to parse these out to the frames/pages???