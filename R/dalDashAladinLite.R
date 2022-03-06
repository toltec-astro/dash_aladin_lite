# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dalDashAladinLite <- function(id=NULL, autoFov=NULL, className=NULL, custom_script_calls=NULL, custom_scripts=NULL, footprintClicked=NULL, footprintHovered=NULL, fov=NULL, layers=NULL, objectClicked=NULL, objectHovered=NULL, options=NULL, position=NULL, style=NULL, survey=NULL, target=NULL) {
    
    props <- list(id=id, autoFov=autoFov, className=className, custom_script_calls=custom_script_calls, custom_scripts=custom_scripts, footprintClicked=footprintClicked, footprintHovered=footprintHovered, fov=fov, layers=layers, objectClicked=objectClicked, objectHovered=objectHovered, options=options, position=position, style=style, survey=survey, target=target)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashAladinLite',
        namespace = 'dash_aladin_lite',
        propNames = c('id', 'autoFov', 'className', 'custom_script_calls', 'custom_scripts', 'footprintClicked', 'footprintHovered', 'fov', 'layers', 'objectClicked', 'objectHovered', 'options', 'position', 'style', 'survey', 'target'),
        package = 'dashAladinLite'
        )

    structure(component, class = c('dash_component', 'list'))
}
