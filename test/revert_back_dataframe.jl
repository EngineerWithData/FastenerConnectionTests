using JSON3, JSON, DataFrames

revert_file = read("src\combine_json\test\combined_data.json", String)

revert_file = JSON.parse(combined_data)