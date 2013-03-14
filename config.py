'''
Configuration file for badge printing routine
'''


#delegates
# uncomment the following to use local data that reflects only fields displayed on badges
delegates = csv_reader("ManualBadges.csv", "utf-8")

# uncomment the following to use local data downloaded from Event Bright
#fields = (3, 2, 4, 19, 6)  #these are data filds to be used for badge creation
#delegates = evb_reader("Attendees-20130225.0247.csv", fields, "utf-8")

#uncomment the following to specify a URL and password to download the data directly
##TODO: implement this
#eventBrightURL= 'something'
#eventBrightPassword = 'secret'

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
   |  |       |XM|       |  |
   |  |_______|  |_______|  |
   |      YM                |
   |   _______    _______   |
   |  |   vm  |  |       |  |
   |  |       |  |hm     |  |
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
  
  We'll assume that a value of 0 will be  top or left justified;
  a value of 100 will be bottom or left justified; a value of 50
  means centered.  
  
  Any other value will be taken literally.  To force a location
  use a incrementally different floating point value - cf. below.

  badge layout
    ________________________
   |tl       tc           tr|
   |                        |
   |                        |
   |cl       cc           cr|
   |                        |
   |                        |
   |bl_______bc___________br|

You can add more, if desired, in the form of ('name', (top, left))
'''

images_locations = [ ('tl', (0, 0)),
                     ('tc', (0, 50)),
                     ('tr', (0, 100)),
                     ('cl', (50, 0)),
                     ('cc', (50, 50)),
                     ('cr', (50, 100)),
                     ('bl', (100, 0)),
                     ('bc', (100, 50)),
                     ('br', (100, 100)),
                     ('logo_top_left_at_center', (50.001, 50.001)) 
                     ]
##TODO: make a dict from image_locations

'''Specify the badges' images here in terms of ("path/to/file", width_, image_location).  Comment out any that
don't apply.  Note: the images will ge proportionately scaled, based on their original width.
'''
images = [ ('organizer_logo', ('./images/organizer_logo.png', 2, 'tc')),
           ('conference_logo', ('./images/conference_logo.png', 0.75, 'bc')),
#           ('top_left', ('./images/generic_image.png', 75, 'tl')),          
#           ('top_center', ('./images/organizer_logo.png', 75, 'tc')),
#           ('top_right', ('./images/organizer_logo.png', 75, 'tr')),
#           ('center_left', ('./images/organizer_logo.png', 75, 'cl')),
#           ('center_center', ('./images/organizer_logo.png', 75, 'cc')),
#           ('center_right', ('./images/organizer_logo.png', 75, 'cr')),
#           ('bottom_left', ('./images/organizer_logo.png', 75, 'bl')),
#           ('bottom_center', ('./images/organizer_logo.png', 75, 'bc')),
#           ('bottom_right', ('./images/organizer_logo.png', 75, 'br')),
           ]
           
#Set fonts to use here in the form of ("field_type", "path/to/font", size, leading, spaceBefore, spaceAfter)
fonts = [ ('bannerFont', ("/Library/Fonts/HeadlineA.ttf", 18, 12, 12, 24)),
          ('nameFont', ("/Library/Fonts/HeadlineA.ttf", 18, 12, 12, 24)),
          ('twitFont', ("/Library/Fonts/GillSans.ttc", 18, 12, 12, 24)),
          ('exhibitorFont', ("Arial Black.ttf", 18, 12, 12, 24)),
          ('vendorFont', ("/Library/Fonts/HeadlineA.ttf", 18, 12, 12, 24)),
          ('sponsorFont', ("/Library/Fonts/HeadlineA.ttf", 18, 12, 12, 24)),
          ('organizerFont', ("/Library/Fonts/HeadlineA.ttf", 18, 12, 12, 24)),
          ]
