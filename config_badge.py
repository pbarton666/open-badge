'''
Configuration file for badge printing routine
'''
#specs for this specific run of badges
##TODO: make this a command line or GUI option
preprinted = False
exhibitor = False

#delegates
#
# uncomment the following to use local data that reflects only fields displayed on badges
#fields correspond to: [first_name, last_name, email, twitter_handle, ticket_type
#    format:  ("/path/to/file/", "encoding", <tag - leave as is>)
#delegates_file = ["ManualBadges.csv", "utf-8", "custom_file"]
delegates_file = ["test_attendees.1730.csv", "utf-8", "custom_file"]

# uncomment the following to use local data downloaded from Event Bright
#fields correspond to: [first_name, last_name, email, twitter_handle, ticket_type
#    format: ("path/to/file/", "encoding", [fields_to_use], <tag - leave as is> )
#delegates_file = ["Attendees-20130225.0247.csv", "utf-8", [3, 2, 4, 19, 6], "eventbright_file")

#uncomment the following to spec a URL/password download eventbright data directly
#    format ("url", "password", <tag - leave as is>)
##TODO: implement this
#delegates_file = ["http://eventgright.com/myconference", "secret", "internet_file"]

#badge geography
#uncomment one of the following to specify english/metric specifications
units = 'inches'   
#units = 'mm'

page_height = 11
page_width = 8.5
'''
    ________________________
   |    label layout        |
   |     TM                 |
   |   _______    _______   |
   |LM|       |  |       |  |
   |  |       |XM|       |  | Page margins
   |  |_______|  |_______|  |
   |      YM                |
   |   _______    _______   |
   |  |   vm  |  |       |  |
   |  |       |  |hm     |  | Badge margins
   |  |_______|  |_______|  |
   |                        |
   |________________________|
'''
#these specs work for standard 3" x 4" six-up sheets, such as Avery 5392
label_width = 4 ; label_height = 3 ; LM = 0.25 ; XM = 0 ; TM = 1; YM = 0

#horizontal and vertical margins for individual badges
hm = .4
vm = .6

'''
Here are some default image locations.  The regions are defined in terms of distance from 
  the top and left, as a percentage of the printable area.  
                                              
               badge layout (w/in margins) 
  _ _ _  _ _ _ _ _ _ _ __     _ _ _ ____ _ _ _ _ _    
 | t l     t c      t r |    |   | = = y1 = = |   |   
 |                      |    |   | = = y2 = = |   | 
 |                      |    |   | = = y3 = = |   |  
 | c l     c c      c r |    |   | = = y4 = = |   |   
 |                      |    |   | = = y5 = = |   |   
 |                      |    |   | = = y6 = = |   |   
 | b l _ _ b c _ _  b r |    |   | = = y7 = = |   |  
                                                   
'''
'''
You can add custom locations in the form of ('name', (top, left)).

We'll assume that the values 0, 50, and 100 take on special meanings.
0 and 100 imply that you want the element justified. (0, 0) means
'top, left justified'.  50 means 'center, if you can'.  If you
specifiy one of these positions and you really mean it, use something
like 0.01, 50.01, or 100.01.  
'''
##TODO: make sure the vertical stuff works w/ the text centering logic
location = [ ('tl', (0, 0)),
                     ('tc', (0, 50)),
                     ('tr', (0, 100)),
                     ('cl', (50, 0)),
                     ('cc', (50, 50)),
                     ('cr', (50, 100)),
                     ('bl', (100, 0)),
                     ('bc', (15, 50)),
                     ('y1', (30, 50)),
                     ('y2', (45, 100)),
                     ('y3', (60, 100)),
                     ('y4', (75, 100)),
                     ('y5', (90, 100)),
                     ('y6', (95, 100)),
                     ('y7', (100, 100)),
                     ('logo_top_left_at_center', (50.001, 50.001)),
                     ('special_ticket_image', (100,100)),
                     ('blob', (100,100)),
                     ]

##TODO:  create logic to plce images at margins

'''Specify the badges' images here in terms of ("path/to/file", width). This provides
a repertoire of images to use in the badge design.
'''

image = [ ('organizer_logo', ('./images/organizer_logo.png', 2)),
           ('conference_logo', ('images/feather.png', 0.75)),
           ('barcode', ('./images/tmp_barcode.png', 1)),         #filename for barcode - not implemented
           ('blob_yellow', ('./images/blob_yellow.png', .75)),          
           ('blog_red', ('./images/blog_red.png', .75)),
           ('blog_green', ('./images/blog_green.png', .75)),
           ('blog_purple', ('./images/blog_purple.png', .75)),
           ('blob_orange', ('./images/blob_orange.png', .75)),
           ('blob_black', ('./images/blob_black.png', .75)),
           ('blob_brown', ('./images/blob_brown', 'blob_brown.png', .75)),
           ]


#these fonts will be used when defining elements of the badge
font = [ ("bannerFont", "/Library/Fonts/HeadlineA.ttf"),
         ("nameFont", "/Library/Fonts/HeadlineA.ttf"),
         ("twitterFont", "/Library/Fonts/GillSans.ttc"),
         ("exhibitorFont", "Arial Black.ttf"),
         ("vendorFont", "/Library/Fonts/HeadlineA.ttf"),
         ("sponsorFont", "/Library/Fonts/HeadlineA.ttf"),
         ("organizerFont", "/Library/Fonts/HeadlineA.ttf"),
         ("tutorialFont", "/Library/Fonts/HeadlineA.ttf"),
         ]
 
#the fields below map the Ticket Type found in the delegate input file to the type of
#   badge we'll issue.  We'll issue one badge per delegate, so the standard badges may
#   be supplemented with additional images, etc.  This provides the possibility to specify
#   a different badge layout for each type of ticket.  If a delegate's ticket type
#   can't be found on this list, it will defalut to "standard"

ticket_type=[ ("Staff", "standard"),
              ("Student Registration", "special"),
              ("mod_pagespeed: Automatic Acceleration for Apache HTTPD", "special"),
              ("Build and Deploy Your Own Big Data Distribution", "special"),
              ("Introducing Apache Traffic Server", "special"),
              ("An Introduction to Plugin Writing for ATS", "special"),
              ("Crash Course on Web Services Security", "special"),
              ("Migrating Complex Applications to OSGI - James to Karaf", "special"),              
              ]


#Set paragraph styles for each of the elements that will appear on the badge. This essentially builds a repertoire
#  that can be accessed later.  Alignment can be "left", "right", or "center".
#Format ["name",("font", "alignment", fontSize, leading, spaceBefore, spaceAfter)

#Note, these settings are further modified in badge_utils::convert_paragraph_style

paragraph_style = [ ('bannerStyle', ("bannerFont", "center", 32, 36, 24, 12)),
                    ('firstNameStyle', ("nameFont", "center", 32, 36, 24, 12)),
                    ('lastNameStyle', ("nameFont", "center", 32, 36, 24, 12)),
                    ('twitterStyle', ("twitterFont", "center", 18, 12, 12, 24)),
                    ('exhibitorStyle', ("exhibitorFont", "center", 18, 12, 12, 24)),
                    ('vendorStyle', ("vendorFont", "center", 18, 12, 12, 24)),
                    ('sponsorStyle', ("sponsorFont", "center",18, 12, 12, 24)),
                    ('organizerStyle', ("organizerFont", "center", 18, 12, 12, 24)),
                    ('tutorialStyle', ("tutorialFont", "center",  18, 12, 12, 24)),
                    ]

#Identify the text fields you may want to use - these should be specified in the same order as the
#   delegate data is provided (cf. delegates section above) - and the paragraph style you want to use.

text_field_format = [('first_name', 'firstNameStyle'),
                     ('last_name', 'lastNameStyle'),
                     ('email', 'twitterStyle'),
                     ('twitter_handle', 'twitterStyle'),
                     ('ticket_type', 'nameStyle'),
               ]

#Lay out the badge formats here.  Special badges can be further tweaked in the "special_badges" section.
#  element is a text_field, image, or (if element can't be identified as a text_field or image) it's
#  interpreted as verbatim text.
#  Format:  ("badge_type", [ ( "element", "location", "(for text items) paragraph_style" ) )

badge_layout = [('standard', [
                            ('organizer_logo', 'tc'),
                            ('conference_logo', 'tl'),
                            ('conference_logo', 'tr'),
                            ('conference_logo', 'br'),
                            ('conference_logo', 'bl'),
                            ('first_name', 'hi', 'nameStyle'),
                            ('last_name', 'mid',  'nameStyle'),
                            ('email', 'top', 'twitterStyle'),
                            ] 
                 ) ,
                ('special_ticket', [
                            ('organizer_logo', 'tc'),
                            ('conference_logo', 'tl'),
                            ('conference_logo', 'tr'),
                            ('conference_logo', 'br'),
                            ('conference_logo', 'bl'),
                            ('first_name', 'hi', 'nameStyle'),
                            ('last_name', 'mid',  'nameStyle'),
                            ('email', 'top', 'twitterStyle'),
                            ] 
                 )               
                ]
               
#Add extra elements to special tickets here. Whether a delegate has a special type will be determined by
#  matching the text supplied below with the Ticket Type field in the input data.  If "collisions"
#  between elements are detected, the system will do its best to remedy, but this is not yet well tested.
#    Format:  ("badge_type", [ ( "element", "location", "(for text items) paragraph_style" ) )

special_ticket = [('Student Registration', [                           
                            ('I am a student', 'cc', 'bannerStyle'), #text element (not id'd as image or named field)
                            ] ) ,
                  ('Apache httpd Basics', [
                              ('blob_black', 'blob'),
                              ] ) ,
                  ('mod_pagespeed: Automatic Acceleration for Apache HTTPD', [
                              ('blob_green', 'blob'),
                              ] ) ,                  
                  ('mod_rewrite Cookbook', [
                              ('blob_orange', 'blob'),
                              ] ) ,
                  ('Build and Deploy Your Own Big Data Distribution', [
                              ('blob_purple', 'blob'),
                              ] ) ,
                  ('Introducing Apache Traffic Server', [
                              ('blob_red', 'blob'),
                              ] ) ,
                  ('An Introduction to Plugin Writing for ATS', [
                              ('blob_yellow', 'blob'),
                              ] ) ,
                  ('Crash Course on Web Services Security', [
                              ('blob_brown', 'blob'),
                              ] ) ,
                  ('Migrating Complex Applications to OSGI - James to Karaf', [
                              ('blob_red', 'blob'),
                              ] ) ,                  
  
                  ]
                  
#if labels are pre-printed, we'll skip any images 
labels_preprintd = False                 
                  
                  
