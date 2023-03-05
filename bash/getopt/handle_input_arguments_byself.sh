#!/bin/bash


# Print usages
print_usage () {
    echo  'Converting media to mp4 format with default H.265 codec'
    echo -e 'Usage :  convert_media [options] -i input_directory  -o output_directory \n'
    echo ' options : '
    echo '      -r     recursively'
    echo '      -v     verbose only'
}

##############################################################################
#    Refer to https://linuxhint.com/bash_operator_examples/  for operators                                     #
#     Refer to https://segmentfault.com/a/1190000021435389  for bash shell arguments              #
##############################################################################

# Handle input arguments 
#       try to wrap in a function but didn't work, maybe later  (need to pass $@ into function or some sort)
#       use function_name  param1 param2  when invoke function, and use $1  $2 ...to access     -->  doesn't take any advantage here because bash has some system variable for input arguments
    
if [[ $# -le 1 ]] ; then
    print_usage 
    exit 1
else
    while [ $# -ge  1 ]; do
     echo “Current parameter: $1”
     shift                                                              # shift can shift the paraemter one position
    done
fi
#    for loop sample 1 :   for ((x=1;x<$#-2;x++))
#
#    args=$@                         This gets all the arguments as array.  $* get arguments as one string
#    args_count=$#            This gets arguments count
#    ${!args_count}             This is how to index specific arguments from arguments array  

