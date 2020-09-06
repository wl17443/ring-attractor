#!/bin/bash

n=$(ls ../backup | wc -l)
mkdir ../backup/batch_$n

mv means.csv ../backup/batch_$n
mv singular_iters/seed_* ..backup/batch_$n
