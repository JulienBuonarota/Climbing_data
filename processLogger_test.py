import subprocess

##
exec_name = "./ProcessLogger/processLogger.sh"
log_file_name = "~/Documents/Climbing_data"
output = subprocess.run("./processLogger.sh -p ananas -S 2", shell=True, capture_output=True)
# cast to bool does not work
# TODO check how to handle b""
process_executed = eval(output.stdout.decode().strip())
