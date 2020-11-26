set terminal png
set output "NonogramBehaviour.png"
set xlabel "Size (n)"
set ylabel "Avg Time (s)"
set logscale y 10
plot "dataNN.res" using 2:4 title 'Algorithm', \