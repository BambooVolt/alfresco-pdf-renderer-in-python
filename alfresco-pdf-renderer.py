#!/usr/bin/env python
# encoding: utf-8
'''
 -- python2.7/3.x wrapper for implementing the alfresco-pdf-renderer (itself a wrapper around PDFium)

It defines a wrapper for generating thumbnails using ImageMagick

@author:     bamboovolt

@copyright:  2017-2019 BambooVolt. All rights reserved.

@license:    Released under a BSD license

@contact:    bamboovolt@ecloud-business-solutions.com
@deffield    updated: 03 November 2019 (0.4 release)

Version History:
0.4 changelog:
Added PATH to beginning of commandline to accomodate launching from native packaged tomcat and using native Magick, gs, etc.

Rationale: The Alfresco All in One installer places ghostscript, magick, etc under /opt/alfresco/common/bin and uses a setenv.sh startup
script to configure this path during tomcat launch.  Since we don't necessarily have that path set in a packaged tomcat instance,
we need magick (convert) to be able to locate ghostscript (gs) at run time, hence this path is required. The easiest method is
this way - it's clunky - we know :)

0.3 changelog:
Initial release

0.2 changelog:
Beta testing - no release

0.1 changelog:
PoC at best - no release
'''

import sys
import os

from optparse import OptionParser

__all__ = []
__version__ = 0.4
__date__ = '2017-10-29'
__updated__ = '2019-11-03'

'''
Set this as required for your environment
'''
PathToGhostscriptEtAl = '/usr/local/bin'

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "1.0" # Keep alfresco happy! This doesn't change and survives changes to this script
    program_build_date = "%s" % __updated__

    program_version_string = '%s' % program_version
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017-2019 BambooVolt (Unincorporated) Licensed under the BSD License"
    program_usage = "%prog [options] input.pdf output.png"

    if argv is None:
        argv = sys.argv[1:]
    
    # We need to extract the commandline options as provided by Alfresco and modify these to suit our ImageMagick equivalent
    try:
        # setup option parser
        parser = OptionParser(usage=program_usage, version=program_version_string, epilog=program_longdesc, description=program_license)
        
        # Fetch desired width and height
        parser.add_option("--height", type="int", dest="height", help="set thumbnail height [default: %default]", default="100", metavar="100")
        parser.add_option("--width", type="int", dest="width", help="set thumbnail width [default: %default]", default="100", metavar="100")
        
        # We don't use this - may be removed in next version
        parser.add_option("--maintain-aspect-ratio", action="store_true", dest="mar", help="set thumbnail aspect ratio [default: %default]", default=False)
        
        # Fetch desired page number
        parser.add_option("--page", type="int", dest="page", help="set page number from which to create thumbnail - page 0 is the 1st page [default: %default]", default="0", metavar="0")
        
        # process options
        (opts, args) = parser.parse_args(argv)

		if len(args) == 2:
            # The example command run at the shell prompt (hence the escaped []'s).  Note the use of the jpeg:size=
            # parameter to speed up the initial document read - unsure if required
            # convert -define jpeg:size=200x200 demo.pdf\[0\] -thumbnail 100x100^ -gravity north -extent 100x100 thumbnail.png
            
			# Prepend the PATH fix in version 0.4 to accomodate various locations for magick, ghostscript, etc.
			cmdline = "PATH=" + PathToGhostscriptEtAl + ":$PATH;/usr/local/bin/convert "

            if opts.width and opts.height:
                cmdline += " -define jpeg:size=%dx%d -thumbnail %dx%d^ -gravity north -extent %dx%d" % (opts.width * 2, opts.height * 2, opts.width,opts.height,opts.width,opts.height)

            if opts.page:
                # We add the page number required - 1 (starts at 0) in square brackets to limit the generation to the
                # first page
                source = args[0] + "[" + str(opts.page) + "]"
            else:
                # No page number supplied - no specs on this but as primary use seems to be thumbnail generation then we'll
                # just default to the first page
                source = args[0] + "[0]"

            cmdline += " " + source + " " + args[1]
        else:
            raise ValueError("Not enough arguments for the input and output files")
        
        # MAIN BODY #

        # Now launch it
        os.system(cmdline)

    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + e.message + "\n")
        sys.stderr.write(indent + "  for help use --help\n\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
