// Builds the component bundle that the Python package (src/) serves to Dash.
// React and ReactDOM are provided by the Dash renderer.
const path = require("path");
const packageJson = require("./package.json");

const dashLibraryName = packageJson.name;

module.exports = (_env, argv) => ({
  entry: { main: "./src/ts/index.ts" },
  output: {
    path: path.resolve(__dirname, "src", dashLibraryName),
    filename: `${dashLibraryName}.js`,
    library: { name: dashLibraryName, type: "window" },
  },
  // The production bundle is committed; it carries no source map.
  devtool: argv.mode === "development" ? "eval-source-map" : false,
  externals: {
    react: "React",
    "react-dom": "ReactDOM",
  },
  resolve: { extensions: [".ts", ".tsx", ".js"] },
  module: {
    rules: [{ test: /\.tsx?$/, use: "ts-loader", exclude: /node_modules/ }],
  },
  performance: {
    // Aladin Lite embeds its WebAssembly core.
    maxAssetSize: 4e6,
    maxEntrypointSize: 4e6,
  },
});
