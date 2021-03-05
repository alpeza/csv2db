import click,sys
from tool import conf
from tool import csvreader

@click.command()
@click.option('--file',required=False, default='', help='CSV to process')
@click.option('--config',required=False, default='', help='Configuration file')
@click.option('--getform',count=True,required=False, help='Shows a sample config form')
def csvsql(config, getform,file):
    if getform:
        print(open("config.yaml", "r").read())
        sys.exit(0)
    if file and config:
        print("Starting ...")
        csv = csvreader.CsvReader(config)
        print("Executing preparation")
        csv.executePrepare()
        print("Executing inserts")
        csv.executeInserts(file)
    else:
        print("[ERROR] --file and --config are mandatory")

if __name__ == '__main__':
    csvsql()
