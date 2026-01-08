from math import log2

DEBUG = 1

with open('raw_data.txt', 'r') as f:
    
    # first line is the header and should be kept
    header_line = f.readline()
    header_line = header_line.rstrip() 

    print( header_line,'\tlog2_sample_A\tlog2_sample_B\tlog2_difference' )
    line_data = []
    for line in f:
        line = line.rstrip()
        line_data = line.split('\t')
        if DEBUG: 
            print( line_data[0],'\t',line_data[4],'\t',line_data[5] ) 

        log2_sample_A = log2( float(line_data[4]) )
        log2_sample_B = log2( float(line_data[5]) )
        log2_difference = abs(log2_sample_A - log2_sample_B)

        if log2_sample_A > 2.0 or log2_sample_B > 2.0 or log2_difference > 3.0 :
            print( line,'\t',log2_sample_A ,'\t',log2_sample_B,'\t',log2_difference)
