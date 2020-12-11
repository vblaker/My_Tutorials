import pandas as pd
import numpy_financial as np
from datetime import date

Interest_Rate = 0.04
Years = 30
Payments_Year = 12
Principal = 200000
Addl_Princ = 50
start_date = (date(2016, 1, 1))

pmt = np.pmt(Interest_Rate/Payments_Year, Years * Payments_Year, Principal)
print(pmt)
