# FastenerConnectionData

This repository contains fastener test data for cold-formed steel connections.

For every test specimen, there is a JSON file with the following data structure:

```julia

struct Source
    authors::Array{String}
    date::Date
    title::String
    bibtex::String
    units::Array{String}
    nominal_data::Vector{String}
    notes::String
end

struct Fastener
    type::Vector{String}
    details::Vector{Dict}
end

struct Ply
    type::Vector{String}
    thickness::Array{Float64}
    elastic_modulus::Array{Any}
    yield_stress::Array{Any}
    ultimate_stress::Array{Any}
end

struct Test
    name::String
    loading::String
    force::Array{Float64}
    displacement::Array{Float64}
end

struct Specimen
    source::Array{Source}
    fastener::Fastener
    ply::Ply
    test::Test
end

```

## Add data

Feel free to open an [issue](https://github.com/runtosolve/FastenerConnectionData/issues) and we will work with you to add your data!

## Data sources

Test results from **bold** references below are available now.   Results from other references are coming soon.  Current total is 552 tests.

* Derveni, Fani, et al. (2021). High-fidelity finite element modeling of wood-sheathed cold-formed steel shear walls. Journal of Structural Engineering 147.2.
* **[Peterman, K. D., N. Nakata, and B. W. Schafer (2014). Hysteretic characterization of cold-formed steel stud-to-sheathing connections. Journal of Constructional Steel Research 101: 254-264.](https://www.sciencedirect.com/science/article/abs/pii/S0143974X14001618)**
* **[Tao, F., Cole, R., Moen, C.D. (2016). Monotonic and cyclic response of single shear cold-formed steel-to-steel and steel-to sheathed connections. Virginia Tech Research Report No. CE/VPI-ST-16/01, American Iron and Steel Institute, Final Report, Washington, D.C.](https://www.researchgate.net/profile/Aritra-Chatterjee-3/publication/333671326_Monotonic_and_Cyclic_Response_of_Single_Shear_Cold-Formed_Steel-to-Steel_and_Sheathing-to-Steel_Connections/links/5cfd974ea6fdccd1308f7ec4/Monotonic-and-Cyclic-Response-of-Single-Shear-Cold-Formed-Steel-to-Steel-and-Sheathing-to-Steel-Connections.pdf)**
* Torabian, S., and B. W. Schafer (2021). Cyclic experiments on sidelap and structural connectors in steel deck diaphragms. Journal of Structural Engineering 147.4.
* **[Zhang, Z., Singh, A., Derveni, F., Torabian, S., Peterman, K. D., Hutchinson, T. C., & Schafer, B. W. (2022). Cyclic experiments on steel sheet connections for standard CFS framed steel sheet sheathed shear walls. Journal of Structural Engineering, 148(2), 04021261.11:33](https://ascelibrary.org/doi/abs/10.1061/%28ASCE%29ST.1943-541X.0003233)**
* **[Zhang, Z., Singh, A., Derveni, F., Torabian, S., Peterman, K. D., Hutchinson, T. C., & Schafer, B. W. (2021). Cyclic experiments on isolated steel sheet connections for CFS framed steel sheet sheathed shear walls with new configurations. Engineering Structures, 244, 112805.](https://www.sciencedirect.com/science/article/abs/pii/S014102962100955X)**






