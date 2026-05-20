# This directory contains datafiles that can be used to test functionality, or simply get an initial look at what the tool will generate.

# NOTE: Keep in mind that the data in examples/output may not have been created with the latest version of the package. Install the package and run the commands below if you want to inspect current functionality. 

# NOTE: Refer to the pkg README if you suspect the commands are also outdated. Please create a GitHub issue if this is the case. :see_no_evil:

```bash
generate_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -o DEVA/src/deva/data/examples/input/deva_files/generate_datadictionary_output.csv
```

```bash
merge_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -dd DEVA/src/deva/data/examples/input/submitted_dd1.csv -o DEVA/src/deva/data/examples/output/merge_datadictionary_dd1_output.csv
```

```bash
merge_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -dd DEVA/src/deva/data/examples/input/submitted_dd2.csv -o DEVA/src/deva/data/examples/output/merge_datadictionary_dd2_output.csv
```
