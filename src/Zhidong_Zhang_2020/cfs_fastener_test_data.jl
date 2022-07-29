using CSV, DataFrames, DataStructures, JSON


data = CSV.File(open(read, raw"src\Zhidong_Zhang_2020\cfs_fastener_test_data.csv")) |> DataFrame


P = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data)

   P = vcat(P, [[0.0, data[i,:P1], data[i,:P2], data[i,:P3], data[i,:P4]]])

end


Δ = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data)

    Δ = vcat(Δ, [[0.0, data[i,:D1], data[i,:D2], data[i,:D3], data[i,:D4]]])

end

data[!,:P] = P

data[!,:Δ] = Δ

data = select!(data, [1:2;11:21])


units = Array{Array{Any, 1}, 1}(undef, 0)
for i = 1:nrow(data)

    units = vcat(units, [[[], [], "mm", "mm", "MPa", "MPa", "MPa", "MPa", "mm", [], [], "kN", "mm"]])

end


insertcols!(data, 3, :units => units)



function convert_dataframe_to_json(data, json_filename)
    all_data_json = [OrderedDict(d[1] => d[2] for d in zip(names(data), data[item, :]))  for item in 1:size(data)[1]]
    stringdata = JSON.json(all_data_json, 4)
    open(json_filename, "w") do f
       write(f, stringdata)
    end
end

json_filename = raw"src\Zhidong_Zhang_2020\cfs_fastener_test_data.json"
convert_dataframe_to_json(data, json_filename)

