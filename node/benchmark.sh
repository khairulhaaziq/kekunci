#!/bin/bash

limits=${1:-1000}
num_words=${2:-25}

export TIMEFORMAT="%R"

print_with_cr() {
  printf "\r%s" "$1"
}
echo "Executing benchmark for limit of ${limits} and ${num_words} generated words..."

#echo "" > node_output.jl
#echo "" > python_output.jl

echo "Running Node.js benchmark:"

[ -e file ] && rm node_times.txt
[ -e file ] && rm node_output.jl
[ -e file ] && rm node_times.txt

for i in {1..100}
do
  print_with_cr "Running ${i}/100..."
  { time node index.js "$limits" "$num_words" > /dev/null; } 2>> node_times.txt
  #python display_charts.py node_output.jl "Node.js" "$i"
done
echo -e "\nAll tests completed, calculating benchmarks..."

echo "Node.js results:"
awk -v limits="$limits" -v num_words="$num_words" '{ sum += $1; if (min == "" || $1 < min) min = $1; if (max == "" || $1 > max) max = $1; } END { if (NR > 0) printf "Total: %.2fs, Average: %.2fs, Min: %.2fs, Max: %.2fs\n", sum, sum/NR, min, max }' node_times.txt

echo "Running Python benchmark:"

[ -e file ] && rm python_times.txt
[ -e file ] && rm python_output.jl
[ -e file ] && rm python_times.txt

for i in {1..100}
do
  print_with_cr "Running ${i}/100..."
  { time python ../random_gen/random_words_jl_2.py "$limits" "$num_words" > /dev/null; } 2>> python_times.txt
  #python display_charts.py python_output.jl "Python" "$i"
done
echo -e "\nAll tests completed, calculating benchmarks..."

echo "Python results:"
awk -v limits="$limits" -v num_words="$num_words" '{ sum += $1; if (min == "" || $1 < min) min = $1; if (max == "" || $1 > max) max = $1; } END { if (NR > 0) printf "Total: %.2fs, Average: %.2fs, Min: %.2fs, Max: %.2fs\n", sum, sum/NR, min, max }' python_times.txt
