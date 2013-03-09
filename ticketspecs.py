#
# In a production environment the use would select the ticket types
# to be blobbed. This is a list of the special tickets that give
# admittance to specific events but do not otherwise require
# identification except for the main event.
#
from reportlab.platypus import Image

specialtickets = ["Migrating Complex Applications to OSGI - James to Karaf",
                "Build and Deploy Your Own Big Data Distribution",
                "Apache httpd Basics",
                "How to Manage Your Apache Product Brand",
                "An Introduction to Plugin Writing for ATS",
                "mod_rewrite Cookbook",
                "Introducing Apache Traffic Server",
                "mod_pagespeed: Automatic Acceleration for Apache HTTPD",
                "Crash Course on Web Services Security"    
]
#
# Again these could relatively easily be user-configured - all the PNG
# files in a given directory would work quite well. For now we are
# happy to make do with a hard-coded list and corresponding file data.
#
# In a perfect world another utility will print out the correspondence
# between ticket names and symbols, and another one will print out
# registers for attendance. This will mean hacking the "read and return
# objects" code out into a separate module for commonality.
#
image_names = "red redsq orangesq orange magenta green cyan bluesq blue black yellow"
ims = []
for color in image_names.split():
    ims.append(Image("images/%s.png" % color, width=25, height=25))   
feather = open("images/feather.png", "rb").read()
bastion = open("images/bastion.png", "rb").read()

if __name__ == "__main__":
	from reportlab.lib.units import inch
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont
	from reportlab.pdfgen  import canvas
	c = canvas.Canvas("Tutorials.pdf")
	for i, (tutorial, image_name) in enumerate(zip(specialtickets, image_names.split())):
		c.drawString(100, 100+30*i, tutorial)
		c.drawImage("images/%s.png" % image_name, 450, 100+30*i, width=25, height=25)
	c.showPage()
	c.save()


