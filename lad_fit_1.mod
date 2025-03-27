set I;

param y{I};
param X{I};

var a;
var b;

var e_pos{I} >= 0;
var e_neg{I} >= 0;

var prediction{i in I} = a * X[i] + b;
s.t. prediction_error{i in I}: e_pos[i] - e_neg[i] == prediction[i] - y[i];

minimize mean_absolute_deviation: sum{i in I}(e_pos[i] + e_neg[i]) / card(I);