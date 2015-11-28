# Isis Web Spider


Isis Web Spider is a Python script to search strings on websites and check if
there are ISIS flags.

Note:
  - To use cv2 install openCV. `sudo apt-get install python-opencv`
  - To use bs4 install BeautifulSoup. `sudo apt-get install python-bs4`

Isis Web Spider does a scan of websites and check if the given strings exists on

Example: ./isiswebspider.py -t targets.txt -s strings.txt -o output.txt -p 1 -i images/

Options:

  - -t the file where are written the targets's URL (one url by line)
  - -s the file where are written the strings to search on the websites
  - -o [optional] The output file to write the results. (one string by line)
    If not given, results will be written in the Terminal
  - -p [optional] To use propagation. By default, during a website scan
    only the links in the same website are checked.
    With the propagation, other websites can be added. In order to
    the program do not works infinitely, the propagation
     is a number. It means the number of times isiswebspider will add others
     websites if it find them.
  - -i [optional] The folder where the pictures will be downloaded to
    checked them
     *This folder has to exist*
