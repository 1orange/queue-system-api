#!/bin/bash

iterations=(100 1000 10000 100000)
for iter in ${iterations[@]}; do
    echo "Simulating ${iter} iterations:"
    python simulator.py --iterations $iter >> /dev/null 2>&1 &
    PID=$!

    echo "Waiting to end of simulation"
    wait $PID

    echo "End of simulation"
done
