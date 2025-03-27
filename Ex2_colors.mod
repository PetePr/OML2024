# each color's content in brown (red, yellow, blue, orange, green, violet)
var x11 >= 0; var x12 >= 0; var x13 >= 0; var x14 >= 0; var x15 >= 0; var x16 >= 0;
# each color's content in gray
var x21 >= 0; var x22 >= 0; var x23 >= 0; var x24 >= 0; var x25 >= 0; var x26 >= 0;
# purchased amounts (orange, green, violet)
var x34 >= 0; var x35 >= 0; var x36 >= 0;

minimize z: 20*x34 + 20*x35 + 20*x36;                   # min price
subject to A1: x11 + x21 = 20;                          # total red color
subject to A2: x12 + x22 = 20;                          # total yellow color
subject to A3: x13 + x23 = 20;                          # total blue color
subject to A4: x14 + x24 = 10 + x34;                    # total orange color
subject to A5: x15 + x25 = 10 + x35;                    # total green color
subject to A6: x16 + x26 = 10 + x36;                    # total violet color
subject to B1: x11 + x12 + x13 + x14 + x15 + x16 >= 50; # total brown
subject to B2: x21 + x22 + x23 + x24 + x25 + x26 >= 50; # total gray
# 4:3 content of red to yellow in brown
subject to C1: 3*(x11 + 0.5*(x14 + x16)) = 4*(x12 + 0.5*(x14 + x15));
# same content of blue and yellow in brown
subject to C2: x12 + 0.5*(x14 + x15) = x13 + 0.5*(x15 + x16); 
# same amount of red and yellow in gray
subject to C3: x21 + 0.5*(x24 + x26) = x22 + 0.5*(x24 + x25);
# 4:3 content of blue to red in gray
subject to C4: 4*(x21 + 0.5*(x24 + x26)) = 3*(x23 + 0.5*(x25 + x26));

solve;
display z;
display x11, x12, x13, x14, x15, x16;
display x21, x22, x23, x24, x25, x26;
display x34, x35, x36;
