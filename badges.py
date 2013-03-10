"""Prints badges from an Eventbrite attendee CSV file.

    Produces a PDF file containing sheets of images for
    Avery 5392. Prints two of each badge alongside to
    make double-sided badge production easier.
"""
exhibitor = False
preprinted = True
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
from badge_utils import evb_reader, blanks, csv_reader

#
# Label Geometry: more of this should be computed
#
##TODO: move to a config file
YS = tuple(x*inch for x in (7.0, 4.0, 1.0))
XS = tuple(x*inch for x in (0.25, 4.25))

LABEL_WIDTH = 4*inch
LABEL_HEIGHT = 3*inch

##TODO:  make this more generic (de-feather it)

feather = PIL.Image.open("images/feather.png")
scaling = 75.0/feather.size[0]
feather = feather.resize(tuple(int(scaling*x) for x in feather.size))
fw, fh = feather.size

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
    VM = 0.4*inch
    HM = 0.6*inch
    for y in YS:
        for x in XS:
            ##TODO: move to a config file
            canvas.drawImage("images/bastion.png",
                    x+(LABEL_WIDTH/2.0)-inch, y+(LABEL_HEIGHT/2.0)-inch,
                    width=2*inch, height=2*inch, preserveAspectRatio=True)
            # canvas.drawImage("images/feather.png",
            #         x, y,
            #         width=0.5*inch, preserveAspectRatio=True)
            for x1 in (HM, LABEL_WIDTH-HM):
                for y1 in (VM, LABEL_HEIGHT-VM):
                    canvas.drawImage("images/feather.png",
                        x+x1-fw/2, y+y1-fh/2, width=fw, height=fh,
                        preserveAspectRatio=True)
            if exhibitor:
                ##TODO: move to a config file
                canvas.setFont("bannerFont", 18)
                for y1 in (VM, LABEL_HEIGHT-VM):
                    twidth = stringWidth("EXHBITOR", "bannerFont", 18)
                    canvas.drawCentredString(x+LABEL_WIDTH/2, y+y1-6, "EXHIBITOR")
    # Finally, restore the canvas back to the way it was.
    canvas.restoreState()
#
# If the following assertion fails you need more images
#
assert len(specialtickets) <= len(ims)
colorblobs = dict(zip(specialtickets, ims))
class Ticket:
    def __init__(self, first, last, email, twitter, typ):
        self.first = first
        self.last = last
        self.email = email
        self.twitter = twitter
        self.type = typ

#
# Build a list of tickets held by each email address
#
tickets = defaultdict(lambda : [])
fields = (3, 2, 4, 19, 6)
#delegates = evb_reader("Attendees-3952423806.csv", fields, "utf-8")
#delegates = evb_reader("Attendees-20130225.0247.csv", fields, "utf-8")
#delegates = blanks(6)
delegates = csv_reader("ManualBadges.csv", "utf-8")
for line in delegates:
    ticket = Ticket(*line)
    tickets[ticket.email].append(ticket)

##TODO: move to a config file
PAGE_HEIGHT=11*inch; PAGE_WIDTH=8.5*inch

ttFile1 = "/Library/Fonts/HeadlineA.ttf"
pdfmetrics.registerFont(TTFont("nameFont", ttFile1))
ttFile2 = "/Library/Fonts/GillSans.ttc"
pdfmetrics.registerFont(TTFont("twitFont", ttFile2))
ttFile3 = "Arial Black.ttf"
pdfmetrics.registerFont(TTFont("bannerFont", ttFile3))
#
# Again, can make paragraph styles user-selectable
#
fsty = ParagraphStyle("name",
                        fontName="nameFont", fontSize=32, leading=36,
                        alignment=TA_CENTER,
                        spaceBefore=24, spaceAfter=12)
lsty = ParagraphStyle("name",
                        fontName="nameFont", fontSize=20, leading=24,
                        alignment=TA_CENTER,
                        spaceBefore=12, spaceAfter=12)
esty = ParagraphStyle("email",
                        fontName="Courier-Bold", fontSize=12.5, leading=18,
                        alignment=TA_CENTER,
                        spaceBefore=12, spaceAfter=12)
tsty = ParagraphStyle("twitter",
                        fontName="twitFont", fontSize=18, leading=24,
                        alignment=TA_CENTER,
                        spaceBefore=12, spaceAfter=12)
#
# Create page template, with the frames for the labels
# created with the bottom corner coordinates
#
frames = []
for y in YS:
    for x in XS:
        frames.append(Frame(x, y, LABEL_WIDTH, LABEL_HEIGHT))
pt = PageTemplate(frames=frames, pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
                    onPage=pageBackground,)
#
# Create the Document template - note that frames are absolutely
# positioned on the page, NOT relative to the margins
#
dt = localDocTemplate("badges.pdf",
             showBoundary=False, pageTemplates=[pt],
             leftMargin=0.0, rightMargin=0.0, topMargin=0.0, bottomMargin=0.0)
#
# The story is simply a label for each attendee
#
story = []
tickets = tickets.items()
tickets.sort(key=lambda t: (t[1][0].first.upper(), t[1][0].last.upper()))
for email, tix in tickets:
    print tix[0].first
    blobs = [colorblobs[t.type] for t in tix if t.type in colorblobs]
    #non_blob_tix = sum(t.type not in colorblobs for t in tix)
    #if non_blob_tix != 1:
    #    print email,  non_blob_tix
    t = tix[0].twitter.strip()
    for _ in "front", "back":
        # MORE ACCURATE, AND AUTOMATED, HEIGHT CALCULATIONS REQUIRED
        # TO ALLOW GENERAL VERTICAL CENTERING OF ARBITRARY LAYOUTS
        if not t:
            story.append(Spacer(inch*3, inch/8.0))
        if not blobs:
            story.append(Spacer(inch*3, inch/5.0))
        story.append(Paragraph(tix[0].first, fsty))
        story.append(Paragraph(tix[0].last, lsty))
        story.append(Paragraph(tix[0].email, esty))
        if t:
            story.append(Paragraph("@"+t, tsty))
        if blobs:
            story.append(Table([blobs]))
        story.append(FrameBreak())
#
# Having created the story, we flow it through the pages
#
dt.build(story)