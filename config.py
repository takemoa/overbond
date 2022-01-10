# Database configuration
DB_NAME = './_db/overbond.db'
TABLE_NAME = 'XICE_BOND'
# How many records to insert in one batch
INSERT_BATCH_SIZE = 5
# LOG_FILE
LOG_FILE = './_log/run.log'

# Configuration of the fields that need to be parsed from the input file
# and of the corresponding database table columns
DATA_CONFIG = {
    # The dictionary key is also the column name
    # SIN	a string prefixed with ISn
    'ISIN': {
        'type': 'string',
        'prefix': 'ISn',
        'notnull': True,  # this must be not null
        'pk': True,  # Primary Key
    },
    # DataDATE	a string prefixed with Dt
    'DataDATE': {
        'type': 'date',
        'prefix': 'Dt',
        'notnull': True,  # this must be not null
        'pk': True,  # Primary Key
    },
    # Name	a string prefixed with NAm in third last or second last of the block
    'Name': {
        'type': 'string',
        'prefix': 'NAm',
        'rows': [7, 8],  # take it only from these rows (0 based)
        'notnull': True,  # this must be not null
        'index': True,  # Index by name
    },
    # Trading Type	a string prefixed with NAm in third row of the block
    'TradingType': {
        'type': 'string',
        'prefix': 'NAm',
        'rows': [2],
    },
    # RIKS	a string prefixed with SNm
    'RIKS': {
        'type': 'string',
        'prefix': 'SNm',
    },
    # Issue Currency	a string prefixed with CUi
    'Issue_Currency': {
        'type': 'string',
        'prefix': 'CUi',
    },
    # Trading Currency	a string prefixed with CUt
    'Trading_Currency': {
        'type': 'string',
        'prefix': 'CUt',
    },
    # Last trading Day	a number sequence prefixed with TTd
    'Last_trading_Day': {
        'type': 'date',
        'prefix': 'TTd',
    },
    # Issuance Date	a string prefixed wtih DIs
    'Issuance_Date': {
        'type': 'date',
        'prefix': 'DIs',
    },
    # Amount Outstanding	a string prefixed with AOs
    'Amount_Outstanding': {
        'type': 'float',
        'prefix': 'AOs',
    },
    # Coupon Rate	a string prefixed with RCp
    'Coupon_Rate': {
        'type': 'float',
        'prefix': 'RCp',
    },
    # Maturity Date	a number sequence prefixed with DNc
    'Maturity_Date': {
        'type': 'date',
        'prefix': 'DNc',
    },
    # Redeem Value	a number prefixed with Mv
    'Redeem_Value': {
        'type': 'float',
        'prefix': 'Mv',
    },
    # Last Coupon Date	a number sequence prefixed with LCOd
    'Last_Coupon_Date': {
        'type': 'date',
        'prefix': 'LCOd',
    },
    # Next Coupon Date	a number sequence prefixed with DNc
    'Next_Coupon_Date': {
        'type': 'date',
        'prefix': 'DNc',
    },
    # Number of Coupons	a number prefixed with CFq
    'Number_of_Coupons': {
        'type': 'float',
        'prefix': 'CFq',
    },
    # Base Value	a number prefixed with VBa
    'Base_Value': {
        'type': 'float',
        'prefix': 'VBa',
    },
    # CleanBid	a number prefixed with BPr
    'CleanBid': {
        'type': 'float',
        'prefix': 'BPr',
    },
    # CleanAsk	a number prefixed with APl
    'CleanAsk': {
        'type': 'float',
        'prefix': 'APl',
    },
    # Last Price	a number prefixed with Pl
    'Last_Price': {
        'type': 'float',
        'prefix': 'Pl',
    },
}