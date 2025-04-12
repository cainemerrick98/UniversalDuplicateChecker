from pandas import DataFrame
import datetime as dt

invoice_columns = ['VendorName', 'Reference', 'Amount', 'Date']
invoice_df = DataFrame(data={
    'ID':['a', 'b', 'c', 'd', 'e'],
    'VendorName':['Parts', 'OfficeSupplies', 'Parts-', 'Parts', 'OfficeSupplies'],
    'Reference':['001', '002', '001', '004', '005'],
    'Amount':[100, 200, 100, 250, 200],
    'Date':[dt.datetime(2025, 1, 1), dt.datetime(2025, 1, 1), dt.datetime(2025, 1, 1), dt.datetime(2025, 2, 1), dt.datetime(2025, 1, 1)]
})