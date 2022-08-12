using JSON3, JSON, DataFrames, JSONTables

filename = raw"src\Tao_et_al_2016\Tao_et_al_2016.json"
json_string = read(filename, String)
json_source = JSON3.read(json_string)
tao_data = DataFrame(jsontable(json_source))

filename = raw"src\Zhang_2020\Zhang_2020.json"
json_string = read(filename, String)
json_source = JSON3.read(json_string)
zhang_data = DataFrame(jsontable(json_source))

combined_data = [tao_data; zhang_data]

function convert_dataframe_to_json(combined_data, json_filename)
    all_data_json = [OrderedDict(d[1] => d[2] for d in zip(names(combined_data), combined_data[item, :]))  for item in 1:size(combined_data)[1]]
    stringdata = JSON.json(all_data_json, 4)
    open(json_filename, "w") do f
       write(f, stringdata)
    end
end

json_filename = raw"src/combine_json/combined_data.json"
convert_dataframe_to_json(combined_data, json_filename)

json_filename = raw"data/fastener_connection_data.json"
convert_dataframe_to_json(combined_data, json_filename)


