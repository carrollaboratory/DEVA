This directory contains datafiles that can be used to test functionality, or simply get an initial look at what the tool will generate.

**NOTE:** Keep in mind that the data in examples/output may not have been created with the latest version of the package. Install the package and run the commands below if you want to inspect current functionality. 

**NOTE:** Refer to the pkg README if you suspect the commands are also outdated. Please create a GitHub issue if this is the case. :see_no_evil:

###  generate_datadictionary
```bash
generate_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -o DEVA/src/deva/data/examples/input/deva_files/generate_datadictionary_output.csv
```


###  merge_datadictionary
```bash
merge_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -dd DEVA/src/deva/data/examples/input/submitted_dd1.csv -o DEVA/src/deva/data/examples/output/merge_datadictionary_dd1_output.csv
```

```bash
merge_datadictionary -df DEVA/src/deva/data/examples/input/submitted_df.csv -dd DEVA/src/deva/data/examples/input/submitted_dd2.csv -o DEVA/src/deva/data/examples/output/merge_datadictionary_dd2_output.csv
```

###  clean_code_column
```bash
clean_code_column -df src/deva/data/examples/input/submitted_df.csv -c other_condition -o src/deva/data/examples/output/submitted_df_cleaned_codes.csv
```

```bash
clean_code_column -df src/deva/data/examples/input/hpo_column.csv -c other_condition -o src/deva/data/examples/output/hpo_column_cleaned_codes.csv
```