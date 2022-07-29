using JSON3, JSON, DataFrames

tao_data = read("src/Tao_et_al_2016/Tao_et_al_2016.json", String)

cfs_data = read("src/Zhidong_Zhang_2020/cfs_fastener_test_data.json", String)

line_break = """\n"""

combined_data = string(tao_data, line_break, cfs_data)

open("src/combine_json/combined_data.json", "w") do f
    write(f, combined_data)
end

open("data/fastener_connection_data.json", "w") do f
    write(f, combined_data)
end
