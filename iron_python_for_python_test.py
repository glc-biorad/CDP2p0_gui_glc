# pythonnet
#import pythonnet
#from pythonnet import load

#load("coreclr")

import clr

clr.AddReference('System.Data')

from System.Data import DataTable

def print_dt_rows(dt):
    print("ID,Lid Number, X, Y, Z, Drip Plate")
    for i in range(dt.Rows.Count):
        dr = dt.Rows[i]
        print("{0}, {1}, {2}, {3}, {4}, {5}".format(
            dr['id'].ToString(),
            dr['lid_number'].ToString(),
            dr['x'].ToString(),
            dr['y'].ToString(),
            dr['z'].ToString(),
            dr['drip_plate'].ToString()
            ))

if __name__ == '__main__':
    # Create an empty DataTable.
    dt = DataTable()
    # Add Columns to the DataTable.
    dt.Columns.Add('id')
    dt.Columns.Add('lid_number')
    dt.Columns.Add('x')
    dt.Columns.Add('y')
    dt.Columns.Add('z')
    dt.Columns.Add('drip_plate')
    # Add a Row to the DataTable.
    dr_0 = dt.NewRow()
    dr_0['id'] = 0
    dr_0['lid_number'] = 1
    dr_0['x'] = -432700
    dr_0['y'] = -970000
    dr_0['z'] = -235000
    dr_0['drip_plate'] = -1198000
    dt.Rows.Add(dr_0)
    # Add one more Row.
    dr_1 = dt.NewRow()
    dr_1['id'] = 1
    dr_1['lid_number'] = 2
    dr_1['x'] = -432700
    dr_1['y'] = -970000
    dr_1['z'] = -265000
    dr_1['drip_plate'] = -1198000
    dt.Rows.Add(dr_1)
    # Display the result.
    print_dt_rows(dt)