param N integer > 0; #the size of the board

# matrix representation of the board where 1 means a queen is placed, 
# 0 means the square is vacant
var x {1..N, 1..N} binary;

# Each row has exactly 1 queen
subject to con1 {i in 1..N}: sum {j in 1..N} x[i, j] = 1;

# Each column has exactly 1 queen
subject to con2 {j in 1..N}: sum {i in 1..N} x[i, j] = 1;

# No two queens on the same main diagonal
subject to con3 {k in -(N-1)..(N-1)}: 
    sum {i in 1..N, j in 1..N: i - j = k} x[i, j] <= 1;

# No two queens on the same anti-diagonal
subject to con4 {k in 2..2*N}: 
    sum {i in 1..N, j in 1..N: i + j = k} x[i, j] <= 1;

option solver gurobi;

#To run, set 
#	param N:='desired value';
#	solve;
#	display x;
# which will show(if exists) an eligible position for chosen N.
