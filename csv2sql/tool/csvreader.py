import csv
from . import conf
import datetime
import mysql.connector
import sys
import logging
import math
from multiprocessing import Process
#logging.basicConfig(filename='example.log',level=logging.DEBUG)

class CsvReader(object):
    """docstring for csvreader."""

    def __init__(self,configfile):
        super(CsvReader, self).__init__()
        self.conf=conf.SQLConfig(file=configfile)

    def read(self,file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.conf.preferences['separator'])
            line_count = 0
            outarr=[]
            for row in csv_reader:
                if line_count < self.conf.preferences['ignorefirst']:
                    line_count += 1
                else:
                    tmp_row={}
                    for el in self.conf.mapping:
                        for key in el:
                            if isinstance(el[key], dict):
                                if 'timeformat' in el[key]:
                                    formato_tiempo = el[key]['timeformat']
                                    valor_celda = row[el[key]['idx']]
                                    dt=datetime.datetime.strptime(valor_celda, formato_tiempo).strftime("%Y-%m-%d %H:%M:%S")
                                    tmp_row[key] = dt
                            else:
                                idx = el[key]
                                tmp_row[key] = row[idx]
                    outarr.append(tmp_row)
                    line_count += 1
            return outarr

    def _initSQLClient(self):
        self.mydb = mysql.connector.connect(
          host=self.conf.db['host'],
          user=self.conf.db['user'],
          port=self.conf.db['port'],
          password=self.conf.db['password'],
          database=self.conf.db['database']
        )
        self.mycursor = self.mydb.cursor()

    def executePrepare(self):
        #print('Executing prepare')
        #print(self.conf.table['prepare'])
        try:
            self._initSQLClient()
            self.mycursor.execute(self.conf.table['prepare'], multi=False)
            self.mydb.commit()
            self.mydb.close()
        except mysql.connector.Error as err:
            pass
            print("Something went wrong: {}".format(err))

    def chunks(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def executeInserts(self,file):
        self._initSQLClient()
        inserts = self.getInserts(file)
        total = len(inserts)
        batch = self.conf.preferences['batch_size']
        total_lotes = math.ceil(total / batch)
        print("-> Tamaño del batch: " + str(batch))
        print("-> Total lotes a procesar: " + str(total_lotes))
        batches = self.chunks(inserts,batch)
        cou=1
        for bat in batches:
            try:
                print("*** Insertando *** " + str(cou) + "/" + str(total_lotes))
                for result in self.mydb.cmd_query_iter(''.join(bat)):
                    pass
                self.mydb.commit()
                cou+=1
            except mysql.connector.Error as err:
                pass
                print("Something went wrong: {}".format(err))
            except Exception as ex:
                pass
        self.mydb.close()

    def getInserts(self,file):
        out=self.read(file)
        table=self.conf.table['name']
        inserts=[]
        for row in out:
            values=[]
            keys=[]
            for el in row:
                keys.append(el)
                values.append("'" + str(row[el]) + "'")
            sql = "INSERT INTO "+table+" ("+','.join(keys)+") VALUES ("+','.join(values)+");"
            inserts.append(sql)
        return inserts

    def printInserts(self,file):
        for ins in self.getInserts(file):
            print(ins)
