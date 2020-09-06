#!/bin/bash

n=$(ls ../backups | wc -l)
mkdir -p ../backups/batch_$n/analysis

mv means.csv ../backups/batch_$n
mv seeds/seed_* ../backups/batch_$n
