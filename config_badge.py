
'''
Configuration file for badge printing routine. The main attributes you'll want to
edit are delegates_file (data source), common_elements (elements on all badges),
badge_layout (elements that differentiate delegates), and special_ticket (elements
added to differentiate different ticket types).

Most of the rest is (or will become after a couple uses) boilerplate.

Note: if you try to specify too many elements, or if any/all won'r fit on the badge,
you'll get a cryptic reportlab.platypus.doctemplate.LayoutError 
error when attempting to build the pdf.  If this happens, 
best bets are to play with the font size and spacing in the paragraph_style section.
'''
#specs for this specific run of badges
##TODO: make this a command line or GUI option
labels_preprintd = False    #True skips image rendering
exhibitor = False
double_badges = True        #True prints side-by-side badges

#**** What do you want to print? ****

#delegates
#
# uncomment the following to use local data that reflects only fields displayed on badges
#fields correspond to: [first_name, last_name, email, twitter_handle, ticket_type
#    format:  ("/path/to/file/", "encoding", <tag - leave as is>)
#delegates_file = ["test_attendees.1730.csv", "utf-8", "custom_file"]
#delegates_file = ["Attendees-20130223.1730.csv", "utf-8", "custom_file"]


# uncomment the following to use local data downloaded from Event Bright
#    fields correspond to: [first_name, last_name, email, twitter_handle, ticket_type
#    format: ("path/to/file/", "encoding", [fields_to_use], <tag - leave as is> )
delegates_file = ["test_attendees.csv", "utf-8", [3, 2, 4, 19, 6], "eventbright_file"]

#uncomment the following to spec a URL/password download eventbright data directly
##TODO:  implement this
#    format ("url", "password", <tag - leave as is>)
#delegates_file = ["http://eventgright.com/myconference", "secret", "internet_file"]


#**** What are you going to print it on? ****
page_height = 11
page_width = 8.5

#uncomment one of the following to specify english/metric specifications
units = 'inches'   
#units = 'mm'

#**** How is your medium set up?  ****
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
#Set margins here (defaults work for Avery 5392 (3"x4" six-up sheets)
label_width = 4 ; label_height = 3 ; LM = 0.25 ; XM = 0 ; TM = 1; YM = 0

#horizontal and vertical margins for individual badges
hm = .1
vm = .1


# **** What slots do you want to identify for your information? ****?
'''
Here are some default image locations.  The regions are defined in terms of distance from 
  the top and left, as a percentage of the printable area.  
                                              
    badge layout (w/in margins) 
  ----------------------     
 | t l     t c      t r |         
 |                      |    
 |                      |   
 | c l     c c      c r |    
 |                      |   
 |                      |    
 | b l _ _ b c _ _  b r |   
  ----------------------                                                     
   0%      50%      100%                                        
   Note:  when elements overlap, the last rendered overwrites any others.
'''

'''
You can add custom locations in the form of ('name', (top, left)).

We'll assume that the values 0, 50, and 100 take on special meanings.
0 and 100 imply that you want the element justified. (0, 0) means
'top, left justified'.  50 means 'center, if you can'.  

Otherwise, these values specify the bottom, left of the element.  If
you want (literally) one of the special values, use a floating 
point equivalent e.g., 0.01, 50.01, or 99.99 (don't go over 100(%)).  
'''

location = [ 
             ('tl', (0, 0)),
             ('tc', (50, 0)),
             ('tr', (100, 0)),
             ('cl', (0, 50)),
             ('cc', (50, 50)),
             ('cr', (100, 50)),
             ('bl', (0, 100)),
             ('bc', (50, 100)),
             ('br', (100, 100)),  
             ('logo_top_left_at_center', (50.001, 50.001)),
             ('special_ticket_image', (100,100)),
             ('blob', (100,100)),                     
                     ]

# **** What images do you want to include? ****?

'''Specify the badges' images here in terms of ("path/to/file", width, height). This provides
a repertoire of images to use in the badge design.  Images used as part of the platypus 'flow'
i.e., added conditionally to individual badges should be in jpg format - Reportlab apparently
doesn't resize others.
'''

image = [ ('organizer_logo', ('./images/bastion.jpg', 2, 2)),
           ('conference_logo', ('./images/feather.png', 0.75, 0.75)),
           ('barcode', ('./images/tmp_barcode.png', 1,1)),         #filename for barcode - not implemented        
           ('blob_red', ('./images/blob_red.jpg', .25, .25)),
           ('blob_green', ('./images/blob_green.jpg', .25, .25)),
           ('blob_purple', ('./images/blob_purple.jpg', .25, .25)),
           ('blob_orange', ('./images/blob_orange.jpg', .25, .25)),
           ('blob_black', ('./images/blob_black.jpg', .25, .25)),
           ('blob_brown', ('./images/blob_brown.jpg', .25, .25)),
           ('tr', ('./images/tr.png', .75, 0.75)),
           ('tl', ('./images/tl.png', .75, 0.75)),
           ('tc', ('./images/tc.png', .75, 0.75)),
           ('br', ('./images/br.png', .75, 0.75)),
           ('bl', ('./images/bl.png', .75, 0.75)),
           ('bc', ('./images/bc.png', .75, 0.75)),
           ('cl', ('./images/cl.png', .75, 0.75)),
           ('cr', ('./images/cr.png', .75, 0.75)),
           ('cc', ('./images/cc.png', .75, 0.75)),
           ]

# ****What fonts do you want to use? ****

'''Some fonts seem to be a bit of an issue.  If you use a font that Reportlib 
does not like, you'll get an error from pdfdoc::Reference.
'''
font = [ ("bannerFont", "./Arial Black.ttf"),
         ("nameFont", "./Arial Black.ttf"),
         ("twitterFont", "./Arial Black.ttf"),
         ("exhibitorFont", "./Arial Black.ttf"),
         ("vendorFont", "./Arial Black.ttf"),
         ("sponsorFont", "./Arial Black.ttf"),
         ("organizerFont","./Arial Black.ttf"),
         ("tutorialFont", "./Arial Black.ttf"),
         ]


#**** What paragraph styles do you want to use? ****

#Set paragraph styles for each of the elements that will appear on the badge. This essentially builds a repertoire
#  that can be accessed later.  Alignment can be "left", "right", or "center".  spaceBefore and spaceAfter refer to the
#  gap between elements.
#Format ["name",("font", "alignment", fontSize, leading, spaceBefore, spaceAfter)

paragraph_style = [ ('bannerStyle', ("bannerFont", "center", 24, 3, 15, 15)),
                    ('firstNameStyle', ("nameFont", "center",24, 36, 15, 15)),
                    ('lastNameStyle', ("nameFont", "center", 24, 36, 15, 15)),
                    ('twitterStyle', ("twitterFont", "center", 14, 12, 15, 15)),
                    ('exhibitorStyle', ("exhibitorFont", "center", 18, 12, 15, 15)),
                    ('vendorStyle', ("vendorFont", "center", 18, 12, 15, 15)),
                    ('sponsorStyle', ("sponsorFont", "center",18, 12, 15, 15)),
                    ('organizerStyle', ("organizerFont", "center", 18, 15, 15, 15)),
                    ('tutorialStyle', ("tutorialFont", "center",  18, 12, 15, 15)),
                    ]

#Note, these settings are further modified in badge_utils::convert_paragraph_style.  If you
#   have any issues to track down, you might look there.


#****  What paragraph styles do you want to assign to your delegate data? ****

text_field = [('first_name', 'firstNameStyle'),
              ('last_name', 'lastNameStyle'),
              ('email', 'twitterStyle'),
              ('twitter_handle', 'twitterStyle'),
              ('ticket_type', 'nameStyle'),
               ]

#****  How do you want the badges to look? ****

#Lay out the badge formats here.  Special badges can be further tweaked in the "special_badges" section.
#  element is a text_field, image, or (if element can't be identified as a text_field or image) it's
#  interpreted as verbatim text.
#  Format:  ("badge_type", [ ( "element", "location", "(for text items) paragraph_style" ) )

#These images are common to all badges 
common_images = [ 
    ('organizer_logo', 'bc'),
#these are special icons for top left, etc. use these to test new setups    
#    ('tl', 'tl'),  
#    ('tr', 'tr'),
#    ('tc', 'tc'),
#    ('br', 'br'),
#    ('bl', 'bl'),
#    ('bc', 'bc'),
#    ('cc', 'cc'),
#    ('cl', 'cl'),
#    ('cr', 'cr'),
]

'''
Use this template to lay out the delegate-specific elements of the badge.  If the 
element specified isn't available (an email address, say), we'll insert an empty spacer.
'spacer<n>' is the percentage of printable vertical area.

The layout can be further customized for special tickets in the next section.  For this 
reason, each line needs to have a unique tag (doesn't matter what it is).

Use one of these formats:

('tag',  'image', spacer<n>)      
('tag',  'text_field', spacer<n>)  
('tag',  'spacer<n>')  
'''
badge_layout = [('null','null'), #leave this - allows something to "insert after"
                ('tag1', 'first_name'),
                ('tag3' , 'last_name'),
                ('tag4','email'),
                ('tag5','twitter_handle'),
                ('end_tag','null'),               
                ]
'''
Extra elements for special tickets.  These can be elements identified as one of the
'image' or 'text_field' defined above.  Alternatively, it can be a line of text.  If
it's text, it needs a 'paragraph_style' from above.

You'll also need to specify where to insert the element - do this by picking
an elment tag to "insert after".  The "insert after" tag can be one here or as 
part of the main 'badge_layout'.

User one of these formats:

[('badge_type', [('tag',  'image', 'insert_after_tag')])       
[('badge_type', [('tag',  'text_field', 'insert_after_tag')])  
[('badge_type', [('tag',  'new_text', 'paragraph_style', 'insert_after_tag')])  

'''

special_ticket = [
    ('Donation to the Apache Software Foundation', [                           
                            ('tag100', 'Donor', 'bannerStyle', 'null'), #Text
                            ('tag100','blob_green', 'end_tag'),
                            ] ) ,
    ('Apache httpd Basics', [
                              ('tag100', 'blob_black', 'end_tag'),  #don't need a style for images
                              ] ) ,
    ('mod_pagespeed: Automatic Acceleration for Apache HTTPD', [
                             ('tag100','blob_green', 'end_tag'),
                              ] ) ,                  
    ('mod_rewrite Cookbook', [
                              ('tag100','blob_orange', 'end_tag'),
                              ] ) ,
    ('Build and Deploy Your Own Big Data Distribution', [
                             ('tag100','blob_purple', 'end_tag'),
                              ] ) ,
    ('Introducing Apache Traffic Server', [
                              ('tag100','blob_red', 'end_tag'),
                              ] ) ,
    ('An Introduction to Plugin Writing for ATS', [
#                              ('tag100','blob_yellow', 'end_tag'),
                              ] ) ,
    ('Crash Course on Web Services Security', [
                              ('tag100','blob_brown', 'end_tag'),
                              ] ) ,
    ('Migrating Complex Applications to OSGI - James to Karaf', [
                             ('tag100','blob_red', 'end_tag'),
                              ] ) ,         
  
                  ]
                  
                
                  
                  
