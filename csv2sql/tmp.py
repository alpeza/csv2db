from tool import conf
from tool import csvreader

cf = conf.SQLConfig()
#cf.print()


csv = csvreader.CsvReader('config.yaml')
#r=csv.read('example.csv')
#print(r)
#csv.printInserts('example.csv')
csv.executePrepare()
csv.executeInserts('example.csv')
