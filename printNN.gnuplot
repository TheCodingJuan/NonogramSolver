set terminal png
set output "NonogramBehaviour.png"
set xlabel "Size (m*n)"
set ylabel "Avg Time (s) Log scale"
set logscale y 10
plot "dataNN.res" using 2:4 title 'Algorithm'