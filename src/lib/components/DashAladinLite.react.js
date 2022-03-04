import React, {Component} from 'react';
import PropTypes from 'prop-types';
import AladinLite from '../private/aladinlite';
import {
    isNil
} from "ramda";


/**
 * DashAladinLite
 */
export default class DashAladinLite extends Component {
    componentDidMount() {

        // event handlers
        var handlers = {
            'select': null,
            'objectClicked': obj => {
                this.props.setProps({objectClicked: obj});
            },
            'objectHovered': obj => {
                this.props.setProps({objectHovered: obj});
            },
            'footprintClicked': obj => {
                this.props.setProps({footprintClicked: obj});
            },
            'footprintHovered': obj => {
                this.props.setProps({footprintHovered: obj});
            },
            'positionChanged': obj => {
                this.props.setProps({position: obj});
            },
            'zoomChanged': obj => {
                this.props.setProps({fov: obj});
            },
            'click': null,
            'mouseMove': null,
            'fullScreenToggled': null
        }
        this.aladin = new AladinLite (this.el, this.props, handlers);
    }

    componentDidUpdate(prevProps) {
        var changedProps = {};
        const {fov, } = this.props;
        // The fov has some inaccuracy so we need to count for that.
        if ((isNil(prevProps.fov)) && (!isNil(fov)) ||
            ((!isNil(prevProps.fov)) && (!isNil(fov)) &&
             ((prevProps.fov / fov <= 0.9) ||
              (prevProps.fov / fov >= (1. / 0.9))) &&
             (fov > 0.)
            )
        ) {
            // update to new fov
            changedProps['fov'] = fov;
        }
        // other changed props
        ["autoFov", "target", "survey", "layers"].forEach(name => {
            if (prevProps[name] !== this.props[name]) {
                changedProps[name] = this.props[name];
            }
        });
        this.aladin.update(changedProps);
    }

    render() {
        return <div
            id={this.props.id}
            style={{
                ...{"width": '500px', "height": '500px'},
                ...this.props.style
            }}
            ref={el => {this.el = el}} />;
    }
}

DashAladinLite.defaultProps = {
    survey: 'P/DSS2/color',
    fov: 10,
    autoFov: false,
    options: {
        "showFullscreenControl": false,
    }
};

DashAladinLite.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,

    /**
     * The class of the container.
     */
    className: PropTypes.string,

    /**
     * The style of the container.
     */
    style: PropTypes.object,

    /**
     * The target to display.
     */
    target: PropTypes.string.isRequired,

    /**
     * The FOV of the display.
     */
    fov: PropTypes.number,

    /**
     * Adjust the fov automatically for target if set to True.
     */
    autoFov: PropTypes.bool,

    /**
     * The survey to display as base image layer.
     */
    survey: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.shape({
            'id': PropTypes.string,
            'name': PropTypes.string,
            'rootUrl': PropTypes.string,
            'cooFrame': PropTypes.oneOf(['equatorial', 'galactic']),
            'maxOrder': PropTypes.number,
            'options': PropTypes.shape({
                'imgFormat': PropTypes.oneOf(['jpeg', 'fits', 'png'])
            })
        })
    ]),

    /**
     * Layers to show.
     * Each layer can be one of types ['catalog', 'overlay', 'moc'].
     */
    layers: PropTypes.arrayOf(
        PropTypes.oneOfType([
            PropTypes.shape({
                'type': PropTypes.oneOf(["catalog"]),
                'data': PropTypes.oneOfType([
                    // hiPSCat
                    PropTypes.string,
                    // records dict
                    PropTypes.arrayOf(PropTypes.shape({
                        "ra": PropTypes.number,
                        "dec": PropTypes.number,
                    }))
                ]),
                'options': PropTypes.shape({
                    'show': PropTypes.bool,
                    'name': PropTypes.string,
                    'color': PropTypes.string,
                    'sourceSize': PropTypes.number,
                    'shape': PropTypes.oneOf([
                        'circle',
                        "plus",
                        "rhomb",
                        'cross',
                        'triangle',
                        'square']),
                    'maxNbsources': PropTypes.number,
                    'raField': PropTypes.string,
                    'decField': PropTypes.string,
                    'displayLabel': PropTypes.bool,
                    'labelColor': PropTypes.string,
                    'labelFont': PropTypes.string,
                    'labelColumn': PropTypes.string,
                    'onClick': PropTypes.oneOf(['showTable', 'showPopup'])
                })
            }),
            PropTypes.shape({
                'type': PropTypes.oneOf(["overlay"]),
                'data': PropTypes.arrayOf(PropTypes.oneOfType([
                    PropTypes.shape({
                        "type": PropTypes.oneOf(['circle']),
                        "ra": PropTypes.number,
                        'dec': PropTypes.number,
                        "radius": PropTypes.number,
                        "color": PropTypes.string
                    }),
                    PropTypes.shape({
                        "type": PropTypes.oneOf(['polyline']),
                        "data": PropTypes.arrayOf(PropTypes.array),
                        "color": PropTypes.string,
                        'lineWidth': PropTypes.number
                    }),
                    PropTypes.shape({
                        "type": PropTypes.oneOf(['polygon']),
                        "data": PropTypes.arrayOf(PropTypes.array),
                    }),

                ])),
                'options': PropTypes.shape({
                    'show': PropTypes.bool,
                    'name': PropTypes.string,
                    'color': PropTypes.string,
                    'lineWidth': PropTypes.number
                })
            }),
            PropTypes.shape({
                'type': PropTypes.oneOf(['moc']),
                'data': PropTypes.oneOfType([
                    // url
                    PropTypes.string,
                    // json
                    PropTypes.object
                ]),
                'options': PropTypes.shape({
                    'show': PropTypes.bool,
                    'name': PropTypes.string,
                    'color': PropTypes.string,
                    'opacity': PropTypes.number,
                    'adaptativeDisplay': PropTypes.bool
                })
            }),

        ])
    ),

    /**
     * Additional options passed to the aladinlite.js
     */
    options: PropTypes.object,

    /**
     * Clicked object.
     */
    objectClicked: PropTypes.object,

    /**
     * Hovered object.
     */
    objectHovered: PropTypes.object,

    /**
     * Clicked footprint.
     */
    footprintClicked: PropTypes.object,

    /**
     * Hovered footprint.
     */
    footprintHovered: PropTypes.object,

    /**
     * Position.
     */
    position: PropTypes.object,
};
