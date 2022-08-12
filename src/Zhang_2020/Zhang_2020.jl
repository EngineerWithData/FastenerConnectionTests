using CSV, DataFrames, DataStructures, JSON


data2 = CSV.File(open(read, raw"src\Zhang_2020\Zhang_2020.csv")) |> DataFrame


P = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data2)

   P = vcat(P, [[0.0, data2[i,:P1], data2[i,:P2], data2[i,:P3], data2[i,:P4]]])

end


Δ = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data2)

    Δ = vcat(Δ, [[0.0, data2[i,:D1], data2[i,:D2], data2[i,:D3], data2[i,:D4]]])

end

data2[!,:P] = P

data2[!,:Δ] = Δ

data2 = select!(data2, [1:4;13:23])


units = Array{Array{Any, 1}, 1}(undef, 0)
for i = 1:nrow(data2)

    units = vcat(units, [[[], [], [], [], "mm", "mm", "MPa", "MPa", "MPa", "MPa", "mm", [], [], "kN", "mm"]])

end


insertcols!(data2, 16, :units => units)



function convert_dataframe_to_json(data2, json_filename)
    all_data_json = [OrderedDict(d[1] => d[2] for d in zip(names(data2), data2[item, :]))  for item in 1:size(data2)[1]]
    stringdata = JSON.json(all_data_json, 4)
    open(json_filename, "w") do f
       write(f, stringdata)
    end
end

json_filename = raw"src\Zhang_2020\Zhang_2020.json"
convert_dataframe_to_json(data2, json_filename)

