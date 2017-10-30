#!/usr/bin/env python
# encoding: utf-8
'''
 -- python2.7 wrapper for implementing the alfreso-pdf-renderer (itself a wrapper around PDFium)

It defines a wrapper for generating thumbnails using ImageMagick

@author:     bamboovolt

@copyright:  2017 BambooVolt. All rights reserved.

@license:    Released under a BSD license

@contact:    bamboovolt@ecloud-business-solutions.com
@deffield    updated: 29 Oct 2017 (Alpha release)
'''

import sys
import os

from optparse import OptionParser

__all__ = []
__version__ = 1.0 # Keep alfresco happy!
__date__ = '2017-10-29'
__updated__ = '2017-10-29'

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "1.0"
    program_build_date = "%s" % __updated__

    program_version_string = '%s' % program_version
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017 BambooVolt (Unincorporated) Licensed under the BSD License"
    
    if argv is None:
        argv = sys.argv[1:]
    
    # We need to extract the commandline options as provided by Alfresco and modify these to suit our ImageMagick equivalent
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        
        # Fetch desired width and height
        parser.add_option("--height", type="int", dest="height", help="set thumbnail height [default: %default]", default="100", metavar="100")
        parser.add_option("--width", type="int", dest="width", help="set thumbnail width [default: %default]", default="100", metavar="100")
        
        # We don't use this - may be removed in next version
        parser.add_option("--maintain-aspect-ratio", action="store_true", dest="mar", help="set thumbnail aspect ratio [default: %default]", default=False)
        
        # Fetch desired page number
        parser.add_option("--page", type="int", dest="page", help="set page number from which to create thumbnail - page 0 is the 1st page [default: %default]", default="0", metavar="0")
        
        # process options
        (opts, args) = parser.parse_args(argv)

	# The example command run at the shell prompt (hence the escaped []'s).  Note the use of the jpeg:size=
        # parameter to speed up the initial document read - unsure if required
        # convert -define jpeg:size=200x200 demo.pdf\[0\] -thumbnail 100x100^ -gravity north -extent 100x100 thumbnail.png
        cmdline = "/usr/local/bin/convert "
        
        if opts.width and opts.height:
            cmdline += " -define jpeg:size=%dx%d -thumbnail %dx%d^ -gravity north -extent %dx%d" % (opts.width * 2, opts.height * 2, opts.width,opts.height,opts.width,opts.height)
        
        if opts.page != "":
            # We add the page number required - 1 (starts at 0) in square brackets to limit the generation to the first page
            source = args[0] + "[" + str(opts.page) + "]"
	else:
            source = args[0]
 
        if len(args) == 2:
            cmdline += " " + source + " " + args[1]
        else:
            print("Not enough arguments for the input and output files")
            return 1
        
        # MAIN BODY #

        # Now launch it
        os.system(cmdline)

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
