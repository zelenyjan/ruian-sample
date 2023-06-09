const path = require("path");
const { readdirSync } = require("fs");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const ESLintPlugin = require("eslint-webpack-plugin");
const StylelintPlugin = require("stylelint-webpack-plugin");
const { VueLoaderPlugin } = require("vue-loader");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const CompressionPlugin = require("compression-webpack-plugin");

// global config
const staticRootFolder = "static";
const staticSrcFolder = `${staticRootFolder}/src`;

// main app config
const defaultAppName = "ruian";
const mainEntryPoint = "main";

// apps
const apps = {
  [defaultAppName]: {
    entry: {
      [mainEntryPoint]: ["./js/index.js", "./scss/main.scss"],
    },
  },
};

const getConfig = (appName) => {
  const prodEnv = process.env.NODE_ENV === "production";
  const outputFolder = prodEnv ? "dist/prod" : "dist/dev";

  return {
    context: path.resolve(__dirname, staticSrcFolder, appName),
    entry: apps[appName].entry,
    devtool: prodEnv ? false : "source-map",
    mode: prodEnv ? "production" : "development",
    watchOptions: {
      poll: 2000,
    },
    plugins: getPlugins(appName, outputFolder, prodEnv),
    output: {
      path: path.resolve(__dirname, staticRootFolder, outputFolder, appName),
      filename: prodEnv
        ? "js/[name].[contenthash].bundle.js"
        : "js/[name].bundle.js",
    },
    devServer: {
      hot: true,
      watchFiles: ["templates/**/*.html"],
      devMiddleware: {
        index: false, // specify to enable root proxying
        writeToDisk: true,
      },
      proxy: {
        context: () => true,
        target: "http://localhost:8000",
      },
      compress: true,
      port: 8080,
    },
    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ["@babel/preset-env"],
            },
          },
        },
        {
          test: /\.vue$/,
          loader: "vue-loader",
        },
        {
          test: /\.(sa|sc|c)ss$/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader,
            },
            {
              loader: "css-loader",
              options: {
                importLoaders: 2,
              },
            },
            "postcss-loader",
            {
              loader: "sass-loader",
              options: {
                additionalData: (content, loaderContext) => {
                  if (appName !== defaultAppName) {
                    return content;
                  }

                  // More information about available properties https://webpack.js.org/api/loaders/
                  const { resourcePath, rootContext } = loaderContext;
                  const relativePath = path.relative(rootContext, resourcePath);

                  if (relativePath === "scss/styles.scss") {
                    return content;
                  }

                  const variablesPath = path.resolve(
                    __dirname,
                    staticSrcFolder,
                    appName,
                    "scss/variables",
                  );
                  return `@import "${variablesPath}";\n` + content;
                },
              },
            },
          ],
        },
      ],
    },
    resolve: {
      extensions: [".js", ".vue"],
      alias: {
        vue$: "vue/dist/vue.esm-bundler",
        src: path.resolve(__dirname, staticSrcFolder, defaultAppName, "js"),
      },
    },
    stats: {
      colors: true,
    },
  };
};

const getCopyPluginPatterns = (appName, outputFolder) => {
  // copy all app's folders except scss and js
  const patterns = [
    {
      from: path.resolve(__dirname, staticSrcFolder, appName),
      to: path.resolve(__dirname, staticRootFolder, outputFolder, appName),
      globOptions: {
        ignore: [`**/${appName}/scss/**`, `**/${appName}/js/**`],
      },
      noErrorOnMissing: true,
    },
  ];

  // copy other apps
  readdirSync(path.resolve(__dirname, staticSrcFolder), { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name)
    .forEach((obj) => {
      if (!(obj in apps) && obj !== "shared") {
        patterns.push({
          from: path.resolve(__dirname, staticSrcFolder, obj),
          to: path.resolve(__dirname, staticRootFolder, outputFolder, obj),
        });
      }
    });

  return patterns;
};

const getPlugins = (appName, outputFolder, prodEnv) => {
  let plugins = [
    new webpack.ProgressPlugin(),
    new ESLintPlugin({ extensions: ["js", "vue"] }),
    new StylelintPlugin(),
    new VueLoaderPlugin(),
    new webpack.DefinePlugin({
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: true,
      "process.env": {},
    }),
    new MiniCssExtractPlugin({
      filename: prodEnv
        ? "css/[name].[contenthash].bundle.css"
        : "css/[name].bundle.css",
    }),
    new CopyPlugin({
      patterns: getCopyPluginPatterns(appName, outputFolder),
    }),
    new BundleTracker({
      path: path.resolve(__dirname, "templates", "webpack"),
      filename: `stats.${appName}.${prodEnv ? "prod" : "dev"}.json`,
    }),
  ];

  if (prodEnv) {
    // production only plugins
    plugins.unshift(new CleanWebpackPlugin());
    plugins.push(
      new CompressionPlugin({
        filename: "[path][base].gz",
        algorithm: "gzip",
        test: /\.(js|css)$/,
        compressionOptions: { level: 9 },
        threshold: 0,
        minRatio: 0.8,
        deleteOriginalAssets: false,
      }),
    );
    plugins.push(
      new CompressionPlugin({
        filename: "[path][base].br",
        algorithm: "brotliCompress",
        test: /\.(js|css)$/,
        compressionOptions: { level: 11 },
        threshold: 0,
        minRatio: 0.8,
        deleteOriginalAssets: false,
      }),
    );
  }
  return plugins;
};

module.exports = () => {
  return getConfig(defaultAppName);
};
