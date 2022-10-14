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
    end
    
    struct Fastener
        type::Vector{String}
        details::Vector{Dict}
    end
    
    struct Ply
        type::Vector{String}
        thickness::Array{Float64}
        elastic_modulus::Array{Float64}
        yield_stress::Array{Float64}
        ultimate_stress::Array{Float64}
    end
    
    struct Test
        name::String
        loading::String
        force::Array{Float64}
        displacement::Array{Float64}
    end

    struct Specimen
        source::Source
        fastener::Fastener
        ply::Ply
        test::Test
    end

```

## Add data

Feel free to open an [issue](https://github.com/runtosolve/FastenerConnectionData/issues) and we will work with you to add your data!

## Data sources

Test results from **bold** references below are available now.   Results from other references are coming soon.

* Derveni, Fani, et al. (2021). High-fidelity finite element modeling of wood-sheathed cold-formed steel shear walls. Journal of Structural Engineering 147.2.
* Peterman, K. D., N. Nakata, and B. W. Schafer (2014). Hysteretic characterization of cold-formed steel stud-to-sheathing connections. Journal of Constructional Steel Research 101: 254-264.
* **[Tao, F., Cole, R., Moen, C.D. (2016). Monotonic and cyclic response of single shear cold-formed steel-to-steel and steel-to sheathed connections. Virginia Tech Research Report No. CE/VPI-ST-16/01, American Iron and Steel Institute, Final Report, Washington, D.C.](https://www.researchgate.net/profile/Aritra-Chatterjee-3/publication/333671326_Monotonic_and_Cyclic_Response_of_Single_Shear_Cold-Formed_Steel-to-Steel_and_Sheathing-to-Steel_Connections/links/5cfd974ea6fdccd1308f7ec4/Monotonic-and-Cyclic-Response-of-Single-Shear-Cold-Formed-Steel-to-Steel-and-Sheathing-to-Steel-Connections.pdf)**
* Torabian, S., and B. W. Schafer (2021). Cyclic experiments on sidelap and structural connectors in steel deck diaphragms. Journal of Structural Engineering 147.4.
* Zhang, Z. , Singh, A., Derveni, F., Torabian, S., Peterman, K. D., Hutchinson, T. C., Schafer, B. W. (2021). Cyclic Experiments on Isolated Steel Sheet Connections for CFS Framed Steel Sheet Sheathed Shear Walls with New Configurations. Engineering Structures, 244, p.112805.
* Zhang, Z., Singh, A., Derveni, F., Torabian, S., Peterman, K. D., Hutchinson, T. C., & Schafer, B. W. (2022). Cyclic Experiments on Steel Sheet Connections for Standard CFS Framed Steel Sheet Sheathed Shear Walls. Journal of Structural Engineering, 148(2), 04021261"





