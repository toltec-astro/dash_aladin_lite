import {
    isNil
} from "ramda";

export default class AladinLite {
    constructor(el, al, handlers) {
        const self = this;
        self.handlers = handlers;
        self.el = el;
        const {A, Aladin, HpxImageSurvey, cds} = window;
        // set the cds catalog toJSON so it does not do circular
        cds.Source.prototype.toJSON = function() {
            const c = this;
            return {
                "catalogName": c.catalog.name,
                "data": c.data,
                "dec": c.dec,
                "isSelected": c.isSelected,
                "isShowing": c.isShowing,
                "marker": c.marker,
                "ra": c.ra,
                "x": c.x,
                "y": c.y
            };
        };
        Circle.prototype.toJSON = function() {
            const c = this;
            return {
                "overlayName": c.overlay.name,
                "id": c.id,
                "isSelected": c.isSelected,
                "isShowing": c.isShowing,
                "centerRaDec": c.centerRaDec,
                "radiusDegrees": c.radiusDegrees
            };
        };
        Polyline.prototype.toJSON = function() {
            const c = this;
            return {
                "overlayName": c.overlay.name,
                "id": c.id,
                "isSelected": c.isSelected,
                "isShowing": c.isShowing,
                "radecArray": c.radecArray,
            };
        };
        Footprint.prototype.toJSON = function() {
            const c = this;
            return {
                "overlayName": c.overlay.name,
                "id": c.id,
                "isSelected": c.isSelected,
                "isShowing": c.isShowing,
                "polygons": c.polygons,
            };
        };
        const {
            target,
            fov,
            autoFov,
            survey,
            layers} = al;
        // save some non-aladin states
        self._target = target;
        self._autoFov = autoFov;

        var init_options = {
            ...Aladin.DEFAULT_OPTIONS,
            ...al.options,
            ...{
                'target': target,
                'fov': fov,
                'survey': self.resolveSurvey(survey)
            }
        };
        // create aladin instance and setup callbacks
        self.aladin = A.aladin("#" + el.id, init_options)
        Object.keys(handlers).forEach(name => {
            self.aladin.on(name, handlers[name]);
        });

        // call self.update for catalog and other stuff
        self.update({
            "layers": layers,
            });
        // some other options
        const {showLayerBox} = al.options;
        if (!isNil(showLayerBox)) {
            self.aladin.showLayerBox();
        }
    };

    resolveSurvey(survey) {
        var _survey = survey;
        if (typeof survey != "string") {
            const {id, name, rootUrl, cooFrame, maxOrder, options} = survey;
            _survey = Aladin.prototype.createImageSurvey(
                id, name, rootUrl, cooFrame, maxOrder, options
            );
        }
        return _survey
    };

    update(changedProps) {
        const self = this;
        var aladin = self.aladin;
        const {
            fov,
            autoFov,
            target,
            survey,
            layers} = changedProps;
        if (!isNil(fov)) {
            aladin.setFoV(fov);
        }
        if (!isNil(autoFov)) {
            self._autoFov = autoFov;
        }
        if (!isNil(survey)) {
            aladin.setBaseImageLayer(self.resolveSurvey(survey));
        }
        if (!isNil(layers)) {
            self.aladin.removeLayers();
            self.addLayers(layers);
        }
        if (!isNil(target)) {
            self._target = target;
            aladin.gotoObject(target);
            if (self._autoFov && isNil(fov)) {
                aladin.adjustFovForObject(self._target)
            }
        }
    };

    addLayers(layers) {
        const self = this;
        const dispatch_fn = {
            "catalog": (data, options) => {
                return self.addCatalog(data, options);
            },
            "overlay": (data, options) => {
                return self.addOverlay(data, options);
            },
            "moc": (data, options) => {
                return self.addMOC(data, options);
            },
        };
        layers.forEach(c => {
            const {type, data, options} = c;
            var layer = dispatch_fn[type](data, options);
            const {show} = options;
            if (!show) {
                layer.hide();
            }
        })
    };

    addCatalog(data, options) {
        const self = this;
        if (typeof data == "string") {
            var catalog = A.catalogHiPS(data, options);
            self.aladin.addCatalog(catalog);
            return catalog;
        }
        // list of records
        var catalog = A.catalog(options);
        var sources = data.map(el => {
            // here we just use the el object itself as the options:
            // ra dec marker popupTitle popupDesc
            // TODO: make the API explicit.
            return A.source(el.ra, el.dec, el, el);
        });
        self.aladin.addCatalog(catalog);
        catalog.addSources(sources);
        return catalog;
    };

    addOverlay(data, options) {
        const self = this;
        var overlay = A.graphicOverlay(options);
        const dispatch_fn = {
            "circle": el => {
                // pass el as options
                return A.circle(el.ra, el.dec, el.radius, el);
            },
            "polyline": el => {
                return A.polyline(el.data, el);
            },
            "polygon": el => {
                return A.polygon(el.data);
            }
        };
        var footprints = data.map(el => {
            return dispatch_fn[el.type](el);
        });
        self.aladin.addOverlay(overlay);
        overlay.addFootprints(footprints);
        return overlay;
    };

    addMOC(data, options) {
        const self = this;
        var moc = null;
        if (typeof data == "string") {
            // url
            moc = A.MOCFromURL(data, options);
        } else {
            // json
            moc = A.MOCFromJSON(data, options);
        }
        self.aladin.addMOC(moc);
        return moc;
    };

}
