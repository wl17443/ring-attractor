#!/bin/bash

n=$(ls ../backups | wc -l)

mv means.csv ../backups/batch_$n
mv seeds/seed_* ../backups/batch_$n
