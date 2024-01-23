first, cd to 'Data_com_opencpn', then <br>
run file with `python -m "Computer_to_OpenCPN.src.main"` <br>
or follow this guideline: <br> 
`cd ./{Path to a folder in repository}` <br>
`python -m "{next folder/or don't if this contains the file you want to run}.src.{to run .py file}` <br>
*/ this is only applicable for files that use relative import path `from ..module1.module2.file import CLASS` <br>
For file that don't use this kind of import, please use `python -u ./{path to file}/file.py`

<br>
Use a serial port generator to make 2 serial ports that can communicate with each other. <br>
One of the port is used in the code to send data and the other will be used in OpenCPN to receive data.