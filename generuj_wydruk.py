import fileinput
from shutil import copyfile
from weasyprint import HTML
import os


# otwarcie pliku i utowrzenie listy
def open_list():
    rlist = open('pacjenci.txt').read().split('\n')
    return rlist

# # funkcja zmieniajaca listę
def clean_list(x):
    x = sorted(list(filter(None, x)))
    x = [e.strip() for e in x]
    return x


patient_list = clean_list(open_list())
# patient_list = open_list()
# tworzenie tabeli do umieszczenia w pliku
def create_table(list):
    table_cell = '<td class="patientname">'
    number_cell = '<tr><td class="number">'
    tmp_table=""
    for i in range(len(patient_list)):
        tmp_table += (number_cell + str(i + 1) + '</td>' + table_cell + patient_list[i] + '</td></tr>')
    return tmp_table

# zapis do pliku
def write_to_file():
    tablecopy = copyfile('misc/table.html', 'misc/pacjenci.html')
    for line in fileinput.FileInput(tablecopy, inplace=1):
        if "<!-- tabelatutaj -->" in line:
            line=line.replace(line, line + create_table(patient_list))
        else:
            pass
        print(line, end='')
    return tablecopy


def create_pdf():
    try:
        os.remove('pacjenci.pdf')
    except:
        pass
    HTML(write_to_file()).write_pdf('pacjenci.pdf')

create_pdf()