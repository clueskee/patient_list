import fileinput
from shutil import copyfile
from weasyprint import HTML
import os
import logging

# Jest jakiś prosty sposób na log po return()?
# Jak sobie poradzić z kolejnością logów?

def open_list():
    """Opens txt file and make a clean list of patients"""
    logging.info('Otwieram listę pacjentów.')
    try:
        with open('pacjenci.txt') as rlist:
            return sorted([patient.strip() for patient in rlist if patient.strip()])
    except OSError as e:
        logging.warning('Błąd pliku pacjenci.txt:', exc_info=True)



def create_table():
    """Generates an HTML table with patients"""
    logging.info('Generuję tabelę z listy pacjentów.')
    table_template = '''<tr>
    <td class="number">{number}</td>
    <td class="patientname">{patient}</td>
    </tr>
    '''
    all_tables=''

    for number, patient in enumerate(open_list(), start=1):
        all_tables += table_template.format(number=number, patient=patient)
    return all_tables

def write_to_file():
    """Writes a HTML table to a copy of template HTML file"""
    logging.info('Zapisuję tabelę z listą pacjentów do pliku.')
    tablecopy = copyfile('misc/table.html', 'misc/pacjenci.html')
    for line in fileinput.FileInput(tablecopy, inplace=1):
        if "<!-- tabelatutaj -->" in line:
            line=line.replace(line, line + create_table())
        else:
            pass
        print(line, end='')
    return tablecopy

def generuj_wydruk():
    """Removes old .pdf file and create newone from teamplate file by weasyprint library""" 
    try:
        os.remove('pacjenci.pdf')
    except OSError as e:
        pass
    HTML(write_to_file()).write_pdf('pacjenci.pdf')

if __name__ == "__main__":
    try:
        os.mkdir('logs')
    except FileExistsError:
        pass
    finally:
        logging.basicConfig(filename='logs/log.log',level=logging.DEBUG, filemode='w', format='%(asctime)s - %(levelname)s():%(lineno)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
        logging.info('Start programu.')
    generuj_wydruk()