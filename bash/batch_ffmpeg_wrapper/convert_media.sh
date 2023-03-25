#!/bin/bash

# default value
RECURSIVE=0
VERBOSE=0
VCODEC='libx265'
INPUT_DIR='.'
OUTPUT_DIR='.'
NEW_FILE_EXTENSION='mp4'
ORIGINAL_FILE_EXTENSION='avi'

supported_codec=('libx265' 'libx264')
supported_source_media_format=('avi' 'mpg' 'mpeg' 'dv' 'mkv' 'flv' 'rm')

# Print usages
print_usage () {
    echo  'Converting media to mp4 format with default H.265 codec'
    echo -e 'Usage :  convert_media [options] -i input_directory  -o output_directory \n'
    echo ' options : '
    echo '      -r  or  --recursive      recursively'
    echo '      -v  or  --verbose       verbose only'
    echo '      -i [input directory]  or --input [input directory]      specify input directory'
    echo '      -o [output directory]  or --output [output directory]      specify onput directory'
    echo '      --vcodec [codec].   video codec.  Default libx265'  
}

handle_input_arguments () {
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
ARGS=$(getopt -o rvi:o:c: --long recursive,verbose,input:,output:,codec: -- $@)
eval set -- "${ARGS}"

while  true ; do
    #echo 'BB' $OPTIND  '$1' $1 '$2'  $2
    case $1 in
        -r|--recursive)
            RECURSIVE=1
            echo "Process -r option" $RECURSIVE
            shift      # shift change the value of $1, but doesn't change the value of $OPT
            ;;
        -v|--verbose)
            VERBOSE=1
            echo "Process -v option" $VERBOSE
            shift
            ;;            
        -c|--codec)
            if [[ ${supported_codec[*]} =~ (^|[[:space:]])$2($|[[:space:]]) ]]; then
                VCODEC=$2
            else
                echo "Support code only : " "${supported_codec[*]}"
                exit1;
            fi
            shift 2
            ;;   
        -i|--input)
            echo "Process -i option with parameter  " $2
            if [ ! -d "$2" ]; then
                echo  "Input directory :  " $2  " does not exist ! "
                exit 1;
            else
                INPUT_DIR=$2
            fi
            shift 2
            ;;
        -o|--output)
            echo "Process -o option with parameter  " $2
            if [ ! -d "$2" ]; then
                echo  "Output directory :  " $2  " does not exist ! "
                exit 1; 
            else    
                OUTPUT_DIR=$2
            fi
            shift 2
            ;;
        --) 
            # stop delimiter for getopt
            # echo "Exit Normally"
            break;
            ;;            
        ? | *) 
            echo "Something incorrect found in provided arguments.."
            exit 1 ;
            ;;
    esac
    #shift
    #echo $1
done
}


walk_dir () {
    
    for pathname in "$1"/*; do
        # if is directory
        if [ -d "$pathname" ]; then

            # create the same folder structure under output directory
	        temp=${pathname//$INPUT_DIR/$OUTPUT_DIR}  
            if [ ! -d "$temp" ]; then
                echo "Creating directory : " $temp
                mkdir "$temp"
            fi

            # if recursive is enable
            if [ $RECURSIVE -eq 1 ];then
                walk_dir "$pathname"
            fi
        # if is a file
        elif [ -e "$pathname" ]; then

            full_filename=$(basename "$pathname")   # this gets the full filename
            extension="${full_filename##*.}"                      # this gets the extension
            filename="${full_filename%.*}"                          # this gets the filename only

            # if the target file extension is in supported medai format arrary
             if [[ ${supported_source_media_format[*]} =~ (^|[[:space:]])$extension($|[[:space:]]) ]]; then
            
		        output_filename=${pathname//$INPUT_DIR/$OUTPUT_DIR}  # change the basepath to output_dir
    		    output_filename=${output_filename//$extension/$NEW_FILE_EXTENSION}  # change the extension
                
                # use eval in the case when filename contains space
                cmd='ffmpeg -i "${pathname}" -vcodec ${VCODEC} "${output_filename}"'
                if [ $VERBOSE -ne 1 ];then
                    eval $cmd
                else 
                    eval echo $cmd
                fi
             else
                    echo  "[MESSAGE] Skipping  ${pathname}"
            fi
                    

        fi
    done
}

#######################################################
# main script starts from here
handle_input_arguments $@

<<COMMENT
echo $RECURSIVE
echo $VERBOSE
echo $VCODEC
echo $INPUT_DIR
echo $OUTPUT_DIR
COMMENT

walk_dir $INPUT_DIR