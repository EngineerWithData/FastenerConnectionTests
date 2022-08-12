using JSON3, JSON, DataFrames, JSONTables

filename = raw"test\combined_data.json"
json_string = read(filename, String)
json_source = JSON3.read(json_string)
data = DataFrame(jsontable(json_source))