
module DashAladinLite
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.1.1"

include("jl/dal_dashaladinlite.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_aladin_lite",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "third_party/jquery-1.10.1.min.js",
    external_url = "https://code.jquery.com/jquery-1.10.1.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "third_party/aladin.min.js",
    external_url = "https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_aladin_lite.min.js",
    external_url = "https://unpkg.com/dash_aladin_lite@0.1.1/dash_aladin_lite/dash_aladin_lite.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_aladin_lite.min.js.map",
    external_url = "https://unpkg.com/dash_aladin_lite@0.1.1/dash_aladin_lite/dash_aladin_lite.min.js.map",
    dynamic = true,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "third_party/aladin.min.css",
    external_url = "https://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css",
    dynamic = nothing,
    async = nothing,
    type = :css
)
            ]
        )

    )
end
end
