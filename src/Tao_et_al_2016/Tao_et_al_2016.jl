using CSV, DataFrames, DataStructures, JSON


data = CSV.File("/Volumes/GoogleDrive/Shared drives/RunToSolve/Professional/AISI/connectiondata/ConnectionData.csv") |> DataFrame


P = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data)

   P = vcat(P, [[0.0, data[i,:fy], data[i,:fc], data[i,:fr], 0.0]])

end


Δ = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data)

    Δ = vcat(Δ, [[0.0, data[i,:dy], data[i,:dc], data[i,:dr], data[i,:df]]])

end

data[!,:P] = P

data[!,:Δ] = Δ

data = select!(data, [1:4;12:22])


units = Array{Array{Any, 1}, 1}(undef, 0)
for i = 1:nrow(data)

    units = vcat(units, [[[], [], [], [], "mm", "mm", "MPa", "MPa", "MPa", "MPa", "mm", [], [], "kN", "mm"]])

end


insertcols!(data, 5, :units => units)



function convert_dataframe_to_json(data, json_filename)
    all_data_json = [OrderedDict(d[1] => d[2] for d in zip(names(data), data[item, :]))  for item in 1:size(data)[1]]
    stringdata = JSON.json(all_data_json, 4)
    open(json_filename, "w") do f
       write(f, stringdata)
    end
end

json_filename = "/Volumes/GoogleDrive/Shared drives/RunToSolve/Professional/AISI/connectiondata/test/connection_data_final.json"
convert_dataframe_to_json(data, json_filename)

