### Shell Scripting

nproc  -> give the number of cpus available
free -g -> give the memory usage
df -h    -> disk size 
top -> gives details of memory disk and cpu usage 

ls -> list all the files and folders
man <command> -> gives the manaul for the command
ls -ltr -> shows all the files with details 
vi -> default available to open the file and write 
touch <file name> -> only creats the file 
mkdir <folder name>-> create the folder 
pwd -> present working directory 


:wq! -> saving the file 
:q! -> close the file without saving it 
cat <file name> -> prints the contents of the file 

sh <file name> -> excutes the file 
./<file name> -> excutes the file 
chmod <rootUser userGroup allUsers > <file name> 4 -> read , 2 ->write, 1 -> excute

set -x # debug mode --> runs all the commands in debug mode

ps -ef --> give the information of all the processes

ps -ef |grep "python" ->ps → Displays currently running processes.
                        -e → Lists all system processes (not just your own).
                        -f → Provides a full-format listing

awk '{print $<column number>}' -> gives the particular column in every row

set -e # exits the script when there is an error
set -o # pipe line fail