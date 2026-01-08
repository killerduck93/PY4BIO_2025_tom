import os
filename = "/tmp/cgifile_" + str(os.getpid())

print("tempfile: %s" % (filename))
