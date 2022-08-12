using CSV, DataFrames, DataStructures, JSON


data1 = CSV.File(open(read, raw"src\Tao_et_al_2016\Tao_et_al_2016.csv")) |> DataFrame


P = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data1)

   P = vcat(P, [[0.0, data1[i,:fy], data1[i,:fc], data1[i,:fr], 0.0]])

end


Δ = Array{Array{Float64, 1}, 1}(undef, 0)
for i =1:nrow(data1)

    Δ = vcat(Δ, [[0.0, data1[i,:dy], data1[i,:dc], data1[i,:dr], data1[i,:df]]])

end

data1[!,:P] = P

data1[!,:Δ] = Δ

data1 = select!(data1, [1:4;12:22])


units = Array{Array{Any, 1}, 1}(undef, 0)
for i = 1:nrow(data1)

    units = vcat(units, [[[], [], [], [], "mm", "mm", "MPa", "MPa", "MPa", "MPa", "mm", [], [], "kN", "mm"]])

end


insertcols!(data1, 16, :units => units)



function convert_dataframe_to_json(data1, json_filename)
    all_data_json = [OrderedDict(d[1] => d[2] for d in zip(names(data1), data1[item, :]))  for item in 1:size(data1)[1]]
    stringdata = JSON.json(all_data_json, 4)
    open(json_filename, "w") do f
       write(f, stringdata)
    end
end

json_filename = raw"src\Tao_et_al_2016\Tao_et_al_2016.json"
convert_dataframe_to_json(data1, json_filename)

