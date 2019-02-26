import pandas as pd
import numpy as np
import sys

# Read file
df = pd.read_csv('记账.csv', parse_dates=['日期'], infer_datetime_format=True, skipinitialspace=True, quotechar='"')

# Modify file to suit format cuz i'm lazy
df = df.drop(['時間戳記'], axis=1)

# iterate over each line
m, n = df.shape

# initialize output dataframe
output = pd.DataFrame(np.zeros([4, 3]), columns=['Spent', 'Paid', 'To Be Paid'],
                      index=['Toby', 'Meng', 'James', 'Lianchun'])

# iterate over each spending, calculate average then associate to appropriate personnel.
i = 0
while i < m:
    no_of_person_involved = 0
    related_personnel = []

    related_personnel = df.iloc[i, 4].split(";", 4)
    no_of_person_involved = len(related_personnel)

    # # Old
    # for j in range(4, 8):
    #     if df.iloc[i, j] == 1:
    #         no_of_person_involved += 1
    #         related_personnel.append(df.columns.values[j])

    # Average
    per_person = df.iloc[i, 3]/no_of_person_involved

    # Paid
    output.loc[df.iloc[i, 0]][1] += df.iloc[i, 3]

    # Assign Spent
    for person in related_personnel:
        output.loc[person][0] += per_person

    i += 1

# Calculate money to be paid
output.iloc[:, 2] = output.iloc[:, 1].to_numpy() - output.iloc[:, 0].to_numpy()

# Check zero sum
TOL = 10**-9
if abs(sum(output.iloc[:, 2].to_numpy())) <= TOL:
    if abs(sum(output.iloc[:, 0].to_numpy()) - sum(output.iloc[:, 1].to_numpy())) <= TOL:
        output = output.round(2)
        output.to_csv('output.csv')
        print("Output Generated.")
else:
    print("Error with output. Check if data is valid:")
    print(df)
    print(output)
