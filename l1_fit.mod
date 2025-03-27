set I;
set J;

param y{I};
param X{I, J};

var a{J};
var b;

var e_pos{I} >= 0;
var e_neg{I} >= 0;

var prediction{i in I} = sum{j in J}(a[j] * X[i, j]) + b;

s.t. prediction_error{i in I}: e_pos[i] - e_neg[i] == prediction[i] - y[i];

minimize mean_absolute_deviation: sum{i in I}(e_pos[i] + e_neg[i]) / card(I);