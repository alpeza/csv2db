# csv2db

Programa para pasar un csv a una base de datos mySQL.

1.- Primero preparamos un `.yaml` con la cofiguración

```yaml
db: #Configuración de la base de datos
  host: localhost
  port: 3307
  user: 'root'
  password: 'root'
  database: 'traiding'
table:
  name: 'lites'
  prepare: | #Script SQL que se ejecutará al inicio
    DROP TABLE IF EXISTS lites;
    CREATE TABLE IF NOT EXISTS `lites` (
      `idlites` INT NOT NULL AUTO_INCREMENT,
      `Time` TIMESTAMP NOT NULL,
      `Symbol` VARCHAR(10) NULL,
      `Open` DECIMAL(18, 10) NULL,
      `High` DECIMAL(18, 10) NULL,
      `Low` DECIMAL(18, 10) NULL,
      `Close` DECIMAL(18, 10) NOT NULL,
      `VolumeLTC` DOUBLE NULL,
      `VolumeKRW` DOUBLE NULL,
      PRIMARY KEY (`idlites`),
      INDEX `TIME` (`Time` ASC))
    ENGINE = InnoDB;
    COMMIT;
preferences:
  ignorefirst: 2 #Numero de primeras filas que se ignoraran
  separator: ',' #Separador del csv
  batch_size: 5000
mapping:        #Mapeo del csv
  - Time:
      idx: 1
      timeformat: '%Y-%m-%d %I-%p'
  - Symbol: 2
  - Open: 3
  - High: 4
  - Low: 5
  - Close: 6
  - VolumeLTC: 7
  - VolumeKRW: 8

```

2.- Ejecutamos, donde file es el fichero csv que deseamos insertar en la bd.

```
./csv2sql.sh --file example.csv --config config.yaml
```
