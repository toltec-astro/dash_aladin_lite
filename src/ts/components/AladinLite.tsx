import React, { useEffect, useRef, useState } from "react";
import A from "aladin-lite";

/** Entity identifier; objects drawn for the same entity share it. */
type EntityId = string | number;

/** Sky position: right ascension and declination in degrees (ICRS). */
type SkyPosition = [number, number];

type Source = {
  id: EntityId;
  ra: number;
  dec: number;
};

type Polyline = {
  type: "polyline";
  id?: EntityId;
  vertices: SkyPosition[];
};

type Polygon = {
  type: "polygon";
  id?: EntityId;
  vertices: SkyPosition[];
};

type Circle = {
  type: "circle";
  id?: EntityId;
  center: SkyPosition;
  radius: number;
};

type Shape = Polyline | Polygon | Circle;

type ImageLayer = {
  type: "image";
  id: string;
  name?: string;
  url: string;
  colormap?: string;
  opacity?: number;
  base?: boolean;
};

type CatalogLayer = {
  type: "catalog";
  id: string;
  name?: string;
  color?: string;
  shape?: "square" | "circle" | "plus" | "cross" | "rhomb" | "triangle";
  source_size?: number;
  sources: Source[];
  visible?: boolean;
};

type GraphicLayer = {
  type: "graphic";
  id: string;
  name?: string;
  color?: string;
  line_width?: number;
  shapes: Shape[];
  visible?: boolean;
};

type Layer = ImageLayer | CatalogLayer | GraphicLayer;

type Props = {
  /** The ID used to identify this component in Dash callbacks. */
  id?: string;
  /** CSS class of the viewer element. */
  className?: string;
  /** CSS style of the viewer element; the viewer fills it, so give it a height. */
  style?: object;
  /** View center: an object name (resolved by Sesame) or "ra dec" in degrees. */
  target?: string;
  /** Field of view, in degrees. */
  fov?: number;
  /** Base HiPS survey, by ID or URL, e.g. "P/DSS2/color". */
  survey?: string;
  /**
   * Aladin Lite options used when the viewer is created, e.g.
   * {"showCooGridControl": true}. Later changes have no effect.
   */
  options?: Record<string, unknown>;
  /**
   * Layers drawn over the survey. Each layer has a unique "id" and a "type":
   * "image" (a FITS image by URL, over the survey or replacing it as the base
   * image), "catalog" (sources with ids), or "graphic" (polylines, polygons
   * and circles). A changed layer is redrawn on top; unchanged layers are
   * kept. See dash_aladin_lite.layers.
   */
  layers?: Layer[];
  /**
   * Ids of the selected entities. A click sets the ids of the objects under
   * the cursor (none on empty sky), a region selection those inside it.
   * Setting it highlights every source and shape with those ids.
   */
  selected_ids?: EntityId[];
  /** Dash-assigned callback that reports property changes to Dash. */
  setProps?: (props: Record<string, unknown>) => void;
};

// Aladin Lite objects and overlays; the library has no types.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AladinObject = any;

type DrawnLayer = {
  key: string;
  remove: () => void;
  selectable: AladinObject[];
  // For a base image: the survey it replaced, restored on removal.
  survey?: AladinObject;
};

// Drawn objects carry the id of their entity in this property.
const ENTITY_ID = "dash_aladin_lite_id";

const tagged = (object: AladinObject, id: EntityId | undefined) => {
  if (id !== undefined) {
    object[ENTITY_ID] = id;
  }
  return object;
};

const drawShape = (shape: Shape) => {
  switch (shape.type) {
    case "polyline":
      return tagged(A.polyline(shape.vertices), shape.id);
    case "polygon":
      return tagged(A.polygon(shape.vertices), shape.id);
    case "circle":
      return tagged(
        A.circle(shape.center[0], shape.center[1], shape.radius),
        shape.id,
      );
  }
};

// Leave options unset when the layer does not give them, so that Aladin Lite's
// defaults apply.
const defined = (options: Record<string, unknown>) =>
  Object.fromEntries(
    Object.entries(options).filter(([, value]) => value !== undefined),
  );

const drawLayer = (
  aladin: AladinObject,
  layer: Layer,
  key: string,
  replaced?: DrawnLayer,
): DrawnLayer => {
  const name = layer.name ?? layer.id;
  switch (layer.type) {
    case "image": {
      const image = A.image(
        layer.url,
        defined({ name, colormap: layer.colormap, opacity: layer.opacity }),
      );
      if (layer.base) {
        // The image replaces the survey until the layer is removed; a base
        // image replacing another keeps the survey to restore.
        const survey = replaced?.survey ?? aladin.getBaseImageLayer();
        aladin.setBaseImageLayer(image);
        return {
          key,
          remove: () => aladin.setBaseImageLayer(survey),
          selectable: [],
          survey,
        };
      }
      aladin.setOverlayImageLayer(image, layer.id);
      return {
        key,
        remove: () => aladin.removeImageLayer(layer.id),
        selectable: [],
      };
    }
    case "catalog": {
      const catalog = A.catalog(
        defined({
          name,
          color: layer.color,
          shape: layer.shape,
          sourceSize: layer.source_size,
        }),
      );
      aladin.addCatalog(catalog);
      const sources = layer.sources.map((source) =>
        tagged(A.source(source.ra, source.dec), source.id),
      );
      catalog.addSources(sources);
      if (layer.visible === false) {
        catalog.hide();
      }
      return {
        key,
        remove: () => aladin.removeOverlay(catalog),
        selectable: sources,
      };
    }
    case "graphic": {
      const overlay = A.graphicOverlay(
        defined({ name, color: layer.color, lineWidth: layer.line_width }),
      );
      aladin.addOverlay(overlay);
      const shapes = layer.shapes.map(drawShape);
      overlay.addFootprints(shapes);
      if (layer.visible === false) {
        overlay.hide();
      }
      return {
        key,
        remove: () => aladin.removeOverlay(overlay),
        selectable: shapes.filter((shape) => ENTITY_ID in shape),
      };
    }
  }
};

/**
 * Aladin Lite sky atlas with layers given as data and selection shared with
 * Dash.
 */
const AladinLite = ({
  id,
  className,
  style,
  target,
  fov,
  survey,
  options,
  layers = [],
  selected_ids = [],
  setProps,
}: Props) => {
  const container = useRef<HTMLDivElement>(null);
  const [aladin, setAladin] = useState<AladinObject>(null);
  // The view values last applied, so that each change is applied once.
  const view = useRef<{ target?: string; fov?: number; survey?: string }>({});
  const drawn = useRef(new Map<string, DrawnLayer>());
  // Events registered once report through the current setProps.
  const report = useRef(setProps);
  report.current = setProps;

  useEffect(() => {
    let cancelled = false;
    A.init.then(() => {
      if (cancelled || !container.current) {
        return;
      }
      const instance = A.aladin(
        container.current,
        defined({
          ...options,
          target,
          fov,
          survey,
        }),
      );
      view.current = { target, fov, survey };
      const select = (ids: EntityId[]) =>
        report.current?.({ selected_ids: ids });
      // A click reports each object under the cursor, then the click itself,
      // also on empty sky. Aladin Lite has then replaced its selection, so the
      // click always reports one, possibly empty.
      let clicked = new Set<EntityId>();
      instance.on("objectClicked", (object: AladinObject) => {
        if (object && ENTITY_ID in object) {
          clicked.add(object[ENTITY_ID]);
        }
      });
      instance.on("click", ({ isDragging }: { isDragging: boolean }) => {
        if (!isDragging) {
          select([...clicked]);
        }
        clicked = new Set();
      });
      instance.on("objectsSelected", (groups: AladinObject[][]) => {
        const ids = new Set<EntityId>();
        for (const object of groups.flat()) {
          if (ENTITY_ID in object) {
            ids.add(object[ENTITY_ID]);
          }
        }
        select([...ids]);
      });
      setAladin(instance);
    });
    return () => {
      cancelled = true;
    };
    // The viewer is created once; later prop changes go to the effects below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (aladin && target !== undefined && target !== view.current.target) {
      aladin.gotoObject(target);
      view.current.target = target;
    }
  }, [aladin, target]);

  useEffect(() => {
    if (aladin && fov !== undefined && fov !== view.current.fov) {
      aladin.setFoV(fov);
      view.current.fov = fov;
    }
  }, [aladin, fov]);

  useEffect(() => {
    if (aladin && survey !== undefined && survey !== view.current.survey) {
      aladin.setImageSurvey(survey);
      view.current.survey = survey;
    }
  }, [aladin, survey]);

  useEffect(() => {
    if (!aladin) {
      return;
    }
    const previous = drawn.current;
    const current = new Map<string, DrawnLayer>();
    for (const layer of layers) {
      const key = JSON.stringify(layer);
      const kept = previous.get(layer.id);
      previous.delete(layer.id);
      if (kept && kept.key === key) {
        current.set(layer.id, kept);
        continue;
      }
      // A base image is replaced directly, without showing the survey between.
      const replaced =
        kept?.survey && layer.type === "image" && layer.base ? kept : undefined;
      if (!replaced) {
        kept?.remove();
      }
      current.set(layer.id, drawLayer(aladin, layer, key, replaced));
    }
    for (const removed of previous.values()) {
      removed.remove();
    }
    drawn.current = current;
  }, [aladin, layers]);

  useEffect(() => {
    if (!aladin) {
      return;
    }
    // Aladin Lite draws selected shapes from its view selection. Its public
    // selectObjects drops the objects in 3.8.2, so set the view's directly.
    const ids = new Set(selected_ids);
    const objects = [...drawn.current.values()]
      .flatMap((layer) => layer.selectable)
      .filter((object) => ids.has(object[ENTITY_ID]));
    if (objects.length > 0) {
      aladin.view.selectObjects([objects]);
    } else {
      aladin.view.unselectObjects();
    }
  }, [aladin, layers, selected_ids]);

  return <div id={id} className={className} style={style} ref={container} />;
};

export default AladinLite;
