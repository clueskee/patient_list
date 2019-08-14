import fileinput
from shutil import copyfile
from weasyprint import HTML
import os
import logging


try:
    # Create logs target Directory
    os.mkdir("logi")
except FileExistsError:
    pass
finally:
    logging.basicConfig(filename='logi/moje_logi.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(funcName)s():%(lineno)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
# :%(lineno)s - %(funcName)20s()
# open txt and generete a list  
def open_list():
    rlist = open('pacjenci.txt').read().split('\n')
    logging.info('poprawnie otwarty plik txt')
    return rlist

#  function to clean the list
def clean_list(x):
    start = len(x)
    x = sorted(list(filter(None, x)))
    x = [e.strip() for e in x]
    logging.info(f'z listy {start}-elementowej  po wyczyszczeniu zostało {len(x)}')
    return x

patient_list = clean_list(open_list())

# make a html table to add to a file
def create_table(list):
    table_cell = '<td class="patientname">'
    number_cell = '<tr><td class="number">'
    tmp_table=""
    for i in range(0, len(patient_list)):
        tmp_table += (number_cell + str(i + 1) + '</td>' + table_cell + patient_list[i] + '</td></tr>')
    return tmp_table

# write tmp_table to temporary file which is copy of a html file with table 
def write_to_file():
    tablecopy = copyfile('misc/table.html', 'misc/pacjenci.html')
    for line in fileinput.FileInput(tablecopy, inplace=1):
        if "<!-- tabelatutaj -->" in line:
            line=line.replace(line, line + create_table(patient_list))
        else:
            pass
        print(line, end='')
    return tablecopy

# making a html file a pdf one
def create_pdf():
    logging.debug('Zaczynamy ')
    try:
        os.remove('pacjenci.pdf')
    except Exception as e:
        logging.warning('błąd pliku pacjenci.txt : {e}')
        pass
    HTML(write_to_file()).write_pdf('pacjenci.pdf')

create_pdf()