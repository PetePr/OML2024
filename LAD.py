# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 21:05:39 2024

@author: Admin
"""
# LAD regression, used for the dataset "Student_performance.csv", in which
#string feature "Extracurricular Activities" was converted to binary for usability.
#As seen from the correlation scores, "Previous scores" appears to be 
#the most impactful of the features, which is later verified in the histogram.
#However, multivariate regression allows to reduce the MAD dramatically even 
#in comparison with this one best feature.

SOLVER = "highs"

from amplpy import AMPL, ampl_notebook

ampl = ampl_notebook(
    modules=["highs"],  # modules to install
    license_uuid="default",  # license to use
)  # instantiate AMPL object and register magics

import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv(
    "Student_performance.csv",
    sep=",", )
students = students.iloc[:247]
for i in range(247):
    if students.loc[i, 'Extracurricular Activities'] == 'No':
        students.loc[i, 'Extracurricular Activities'] = 0
    else:
        students.loc[i, 'Extracurricular Activities'] = 1 

print(students.corr()['Performance Index'])

def lad_fit_1(df, y_col, x_col):
    m = AMPL()
    m.read("lad_fit_1.mod")

    m.set["I"] = df.index.values

    m.param["y"] = df[y_col]
    m.param["X"] = df[x_col]

    m.option["solver"] = SOLVER
    m.eval( r"""option solver_msg 0;""" )
    m.solve()

    return m

m = lad_fit_1(students, "Performance Index", "Previous Scores")

print(f'The mean absolute deviation for a single-feature regression is {m.obj["mean_absolute_deviation"].value():0.5f}')

mad = (students["Previous Scores"] - students["Previous Scores"].mean()).abs().mean()
vars = {}
for i in students.columns:
    m = lad_fit_1(students, "Performance Index", i)
    vars[i] = m.obj["mean_absolute_deviation"].value()

fig, ax = plt.subplots()
pd.Series(vars).plot(kind="bar", ax=ax, grid=True)
ax.axhline(mad, color="r", lw=3)
ax.set_title("MADs for single-feature regressions")

students["prediction"] = [i[1] for i in m.var["prediction"].get_values()]
students["Performance Index"].hist(label="data")

students.plot(x="Performance Index", y="prediction", kind="scatter")
plt.show()

def l1_fit(df, y_col, x_cols):
    m = AMPL()
    m.read("l1_fit.mod")

    m.set["I"] = df.index.values
    m.set["J"] = x_cols

    m.param["y"] = df[y_col]
    m.param["X"] = df[x_cols]

    m.option["solver"] = SOLVER
    m.solve()

    return m


m = l1_fit(
    students,
    "Performance Index",
    [
        "Previous Scores",
        "Hours Studied",
        "Extracurricular Activities",
        "Sleep Hours",
        "Sample Question Papers Practiced",
    ],
)
print(f"MAD = {m.obj['mean_absolute_deviation'].value():0.5f}\n")

for k, v in m.var["a"].get_values():
    print(f"{k} {v}")
print("\n")

students["prediction"] = [i[1] for i in m.var["prediction"].get_values()]
students["Performance Index"].hist(label="data")

students.plot(x="Performance Index", y="prediction", kind="scatter")
plt.show()

