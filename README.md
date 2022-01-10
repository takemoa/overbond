# Overbond Coding Challenge

This repository contain the completed coding (director level) challenge as documented in https://github.com/overbond/overbond-eng-test/blob/main/director.md

The implementation is in Python and was developed with Python 3.9.4 however any version greater than 3.7 should work. Only standard Python libraries are required to run this program.

The SQL database used is SQL Lite 3. The database is automatically created on first run of the program.

## Execution

Clone this repository and execute the following command in the directory where the code has been cloned:

```sh

python run.py <input_file_path>

```

where *input_file_path* is the data file path either absolute or relative to current directory, e.g.

```sh

python run.py .\_data\XICE_Bond_Close2.tip

```

## Configuration

The program configuration is in *config.py* and contains the following configuration values:

### Database Configuration

``` python
# The location of the sql lite database file
DB_NAME = './_db/overbond.db'
# The name of the table where the records are created. The table is created dynamically based on the DATA_CONFIG values
TABLE_NAME = 'XICE_BOND'

# How many records to insert in one batch
INSERT_BATCH_SIZE = 5
```

### Log Configuration
``` python
# The path of the log file
LOG_FILE = './_log/run.log'
```

### Data Configuration

The data (input file, target sql table) is configured through DATA_CONFIG dictionary. Each item in the dictionary corresponds to one field of interest from the data file record
and also to a column in the target datbase table. The key in the data dictionary is the name of the field and also the name of the corresponding table column.
For example:

``` python
DATA_CONFIG = {
    # SIN	a string prefixed with ISn
    'ISIN': {
        'type': 'string',
        'prefix': 'ISn',
        'notnull': True,  # this must be not null
        'pk': True,  # Primary Key
    },
    # ...
    # Name	a string prefixed with NAm in third last or second last of the block
    'Name': {
        'type': 'string',
        'prefix': 'NAm',
        'rows': [7, 8],  # take it only from these rows (0 based)
        'notnull': True,  # this must be not null
        'index': True,  # Index by name
    },
    # ...
}
```
The configuration values for each field are:

- *type*: the type of the field. Allowed values are *string*, *float*, *int* and *date*. The *date* fields are expected to be in format YYYYMMDD, e.g. 20220706.
DURING parsing the field values are converted to the type specified and inserted into the database accordingly using the corresponding SQL type, e.g.
*date* type translates to *DATETIME* SQL type.
- *prefix*: the prefix of this field in the source data file
- *rows*: optional, what rows (0 to 9) to take this values from
- *pk*: optional, whether this field should be part of the Primary Key
- *notnull*: optional, whether this field should be not null
- *index*: optional, whether this field should be indexed or not

# Parsing
The parsing process is dynamic and based on the rules defined in the *DATA_CONIG* dictionary. Passing an invalid file will more likely result in no records being
created in the database

## Database

A SQL Lite 3 database is created automatically if one does not exist. If using the defaul configuration the database is created at ./_db/overbond.db

The database table and indexes are created dinamically based on the rules defined in the *DATA_CONFIG*. If the default configuration values (as downloaded from github)
are used, the target table will have:
- a composite primary key: ISIN and DataDATE
- an index on the not null column: Name
- datetime fields: DataDATE, Last_trading_Day, Issuance_Date, Maturity_Date, Last_Coupon_Date, Next_Coupon_Date
- all columns optional except the primary key and index columns

With the defaul configuration the following SQL statements (also available in the log file) are executed:

```sql

CREATE TABLE IF NOT EXISTS XICE_BOND( 
  ISIN TEXT NOT NULL,
  DataDATE DATETIME NOT NULL,
  Name TEXT NOT NULL,
  TradingType TEXT,
  RIKS TEXT,
  Issue_Currency TEXT,
  Trading_Currency TEXT,
  Last_trading_Day DATETIME,
  Issuance_Date DATETIME,
  Amount_Outstanding REAL,
  Coupon_Rate REAL,
  Maturity_Date DATETIME,
  Redeem_Value REAL,
  Last_Coupon_Date DATETIME,
  Next_Coupon_Date DATETIME,
  Number_of_Coupons REAL,
  Base_Value REAL,
  CleanBid REAL,
  CleanAsk REAL,
  Last_Price REAL,
	PRIMARY KEY (ISIN, DataDATE)
)

CREATE INDEX IF NOT EXISTS XICE_BOND_Name_index ON XICE_BOND(Name)

```

## Logging
The logging is done using the standard Python logging library. Log messages from INFO up are logged in the console, while in the log file it is more information
with messages starting from the DEBUG level.

Console:

``` logtalk
root 2022-01-09 21:01:35,642 INFO Database created and successfully connected to: ./_db/overbond.db
root 2022-01-09 21:01:35,642 INFO SQLite Database Version is: [('3.37.0',)]
root 2022-01-09 21:01:35,643 INFO XICE_BOND table is setup - (0,) existing records
root 2022-01-09 21:01:35,643 INFO Processing file ./_data/XICE_Bond_Close2.tip
root 2022-01-09 21:01:35,648 INFO - 5 records
...
```

Log file:

``` logtalk
...
root 2022-01-09 19:32:47,361 INFO XICE_BOND table is setup - (0,) existing records
root 2022-01-09 19:32:47,361 INFO Processing file _data/XICE_Bond_Close2.tip
root 2022-01-09 19:32:47,361 DEBUG Parsing a new record
root 2022-01-09 19:32:47,361 DEBUG - row 0: ['BDSr', 'i2', 'NAmGITS', '\n']
root 2022-01-09 19:32:47,361 DEBUG - row 1: ['BDx', 'i138', 'Si6', 's2', 'SYmIS', 'NAmNasdaq Iceland hf.', 'CNyIS', 'MIcXICE', '\n']
root 2022-01-09 19:32:47,361 DEBUG - row 2: ['BDm', 'i896', 'Si006178', 's2', 'Ex138', 'NAmIceland Cash Bond Trading', 'SYmICECB', 'TOTa+0000', 'LDa20190406', 'MIcXICE', '\n']
root 2022-01-09 19:32:47,361 DEBUG - row 3: ['BDIs', 'i15096', 'SiKOP', 's2', 'ISsKOP', 'NAmKópavogsbær', 'CNyIS', 'MLEi254900VH50SHJW5ROH12', '\n']
root 2022-01-09 19:32:47,362 DEBUG - row 4: ['BDt', 'i8169', 'SiKOP_96_1A', 's2', 'Ex138', 'Mk896', 'INiKOP004ICECBCSH', 'SYmKOP 96 1A', 'NAmKópavogsbær 96 1A', 'SNmKOP 96 1A', 'ISnIS0000003952', 'ISi15096', 'ISsKOP', 'CUiISK', 'CUtISK', 'PRt3', 'VOd2', 'LDa20001028', 'Cf1', 'TTd20211128', 'CFcDNFUFR', 'IEtEqual installments', 'NMv1', 'ITSz347', 'NDp4', 'NDc3', 'MPmN', 'MPaN', 'NDTp4', 'NDTc3', 'CLId21232', 'CNyIS', 'ITStN', 'SSc2', 'STy4', 'AUmY', 'TRaY', 'INrY', 'PTaN', 'PTb2', 'OXCl0', 'RLoY', 'IaN', 'FxN', 'IqN', 'TUsN', 'MSc444', 'LSz5000000', '\n']
root 2022-01-09 19:32:47,362 DEBUG - row 5: ['BDu', 'i8169', 'SiKOP_96_1A', 's2', 'IICtISIN', 'FISnKOPAVOGSBAER/5.0 BD 20211128', 'MIFrBOND', 'MCTyOTHR', 'MLIqN', 'MTcN', 'MLPr100000000', 'MLPo0', 'MSPo0', 'MJCjN', 'MQu10000', 'MBTyOEPB', 'MBPs0', 'MCStN', '\n']
root 2022-01-09 19:32:47,363 DEBUG - row 6: ['BDBo', 'i8169', 'SiKOP_96_1A', 's2', 'BTy1', 'DIs19960608', 'AOs700000000', 'DMa20211128', 'RCp5', 'DNc20211128', 'DCm1', 'Mv100', 'HaY', 'RDd0', 'RDt1', 'NRd2', 'CPFrN', 'LCOd20211128', 'Fv1', 'CFq2', 'Cc8', 'RIxCPI_IS', 'FCd19980528', 'VBa175.8', 'Vm5000000', 'MDo255', 'SSDaN', 'FIt3', 'DAd19960515', '\n']
root 2022-01-09 19:32:47,363 DEBUG - row 7: ['BDLi', 'i14718', 'SiISMB', 's2', 'LSt433', 'SYmISMB', 'NAmICE Municipal and LSS Bonds', 'LCyISK', 'TCeY', '\n']
root 2022-01-09 19:32:47,363 DEBUG - row 8: ['BDLi', 'i14720', 'SiICE_MUNICIPAL_AND_LSS_BONDS', 's2', 'LSt434', 'PAi14718', 'NAmICE Municipal and LSS Bonds', 'LCyISK', 'TCeN', '\n']
root 2022-01-09 19:32:47,363 DEBUG - row 9: ['m', 'i8169', 't180000.336', 'Dt20210907', 'ISOcY', 'ISOtY', '\n']
root 2022-01-09 19:32:47,363 DEBUG - parsed fields:
 {'TradingType': 'Iceland Cash Bond Trading', 'RIKS': 'KOP 96 1A', 'ISIN': 'IS0000003952', 'Issue_Currency': 'ISK', 'Trading_Currency': 'ISK', 'Last_trading_Day': datetime.datetime(2021, 11, 28, 0, 0), 'Issuance_Date': datetime.datetime(1996, 6, 8, 0, 0), 'Amount_Outstanding': 700000000.0, 'Coupon_Rate': 5.0, 'Maturity_Date': datetime.datetime(2021, 11, 28, 0, 0), 'Next_Coupon_Date': datetime.datetime(2021, 11, 28, 0, 0), 'Redeem_Value': 100.0, 'Last_Coupon_Date': datetime.datetime(2021, 11, 28, 0, 0), 'Number_of_Coupons': 2.0, 'Base_Value': 175.8, 'Name': 'ICE Municipal and LSS Bonds', 'DataDATE': datetime.datetime(2021, 9, 7, 0, 0)}
root 2022-01-09 19:32:47,363 DEBUG - fields not found: ['CleanBid', 'CleanAsk', 'Last_Price']

```
