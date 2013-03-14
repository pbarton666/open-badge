"""
badge_utils.py: utility functions for badge printer input
"""
import codecs
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY


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
    assert pos == len(line) # sanity check
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
        yield tuple(cols+["manual"])

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
            for k, v in fonts.iteritems():
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
    
def add_units(config):
    '''
    Adds units object (specified in inches or mm) to the paper/label dimensions. The "units"
    come from reportlab.lib.units (added to the config dict with configReader::confReader).
    This makes the mainline code a bit more flexible and easy to read.
    '''
    media = config['media_specs']  #note this a "live" copy of config; updates to media also update config
    units = config['units']

    #important note to self.  You CANT simply iterate thru a dict an update it.  The deck can get reshuffled with
    #   every update - doubling up on some and leaving others out (potentially)
    pending_updates =[]
    for spec, value in media.iteritems():    
        pending_updates.append((spec, value*units))
    for p in pending_updates:
        media.update({p[0]:p[1]})
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
'''
def read_delegate_file(config):
    #calls appropariate reader, returns a list of delegates
    filename, encoding, filetype = config['delegates_file']
    if filetype =="custom_file":
        return csv_reader(filename, encoding)
    if filetype =="eventbright_file":
        return evb_reader(filename, encoding)   
    if filetype =="internet_file":
        print "sorry, not yet implented"
        return evb_reader(filename, encoding)  
    return -1
    
    #delegates_file = ["test_attendees.1730.csv", "utf-8", "custom_file"]
'''
def generate_blobs(config):
    #may generate color blobs someday
    return config
'''
>>> config['paragraph_style']
{'organizerStyle': ('bannerFont', 'center', 18, 12, 12), 
'vendorStyle': ('bannerFont', 'center', 18, 12, 12), 


tsty = ParagraphStyle("twitter",
                        fontName="twitFont", fontSize=18, leading=24,
                        alignment=TA_CENTER,
                        spaceBefore=12, spaceAfter=12)
'''