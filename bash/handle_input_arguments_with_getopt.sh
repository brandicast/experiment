#!/bin/bash


# Print usages
print_usage () {
    echo  'Converting media to mp4 format with default H.265 codec'
    echo -e 'Usage :  convert_media [options] -i input_directory  -o output_directory \n'
    echo ' options : '
    echo '      -r     recursively'
    echo '      -v     verbose only'
    echo '      -i     input directory'
    echo '      -o    output directory'
}

##############################################################################
#    Refer to https://linuxhint.com/bash_operator_examples/  for operators                                     #
#     Refer to https://segmentfault.com/a/1190000021435389  for bash shell arguments              #
##############################################################################

#  $#  :  number of arguments
#  $*  :   merge arguments as string
#   $* != "-"*   :   If the string does not start with -

#  Check command line arguments is provided and started with '-' ,   if not, show help messages
#   Not the bracket has to be written in the following way


if  [[ $* != "-"* || $# -eq 0 ]]  
then
    print_usage
    exit 1;
fi

#eval set -- "$VALID_ARGS"
#echo $VALID_ARGS

#  Note :   There are difference between getopts  and getopt
#

# Don't understand why it has to be like below.....
ARGS=$(getopt -o rvi:o: --long recursive,verbose,input:,output: -- $@)
eval set -- "${ARGS}"

while  true ; do
    #echo 'BB' $OPTIND  '$1' $1 '$2'  $2
    case $1 in
        -r|--recursive)
            echo "Process -r option"
            shift      # shift change the value of $1, but doesn't change the value of $OPT
            ;;
        -v|--verbose)
            echo "Process -v option"
            shift
            ;;            
        -i|--input)
            echo "Process -i option with parameter  " $2
            if [ ! -d "$2" ]; then
                echo  "Input directory :  " $2  " does not exist ! "
                exit 1;
            fi
            shift 2
            ;;
        -o|--output)
            echo "Process -o option with parameter  " $2
            if [ ! -d "$2" ]; then
                echo  "Output directory :  " $2  " does not exist ! "
                exit 1;  
            fi
            shift 2
            ;;
        --) 
            echo "Exit Normally"
            exit 1 ;
            ;;            
        ? | *) 
            echo "Something incorrect found in provided arguments.."
            exit 1 ;
            ;;
    esac
    #shift
    #echo $1
done
