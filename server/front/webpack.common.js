const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const TerserPlugin = require("terser-webpack-plugin");
const webpack = require('webpack');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const common = {
  entry: {
    console: "./src/entrypoints/console.jsx",
    docs: "./src/entrypoints/docs.jsx",
    index: "./src/entrypoints/index.jsx",
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            plugins: [
              ["@babel/transform-runtime"],
            ],
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
            ],
          },
        },
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader'
          },
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass'),
            },
          },
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'images',
            },
          },
        ],
      },
      {
        test: /\.(woff|woff2|ttf|otf|eot)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'fonts',
            },
          },
        ],
      },
    ],
  },
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "../public/static"),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
  ],
  resolve: {
    extensions: [".js", ".jsx"],
  },
  stats: {
    children: true,
    colors: true,
    modules: true,
  },
};

const dev = {
  ...common,
  devtool: "source-map",
  entry: {
    console: [
      "webpack-dev-server/client?https://localhost:8401",
      "webpack/hot/only-dev-server",
      "./src/entrypoints/console.jsx",
    ],
    docs: [
      "webpack-dev-server/client?https://localhost:8401",
      "webpack/hot/only-dev-server",
      "./src/entrypoints/docs.jsx",
    ],
    index: [
      "webpack-dev-server/client?https://localhost:8401",
      "webpack/hot/only-dev-server",
      "./src/entrypoints/index.jsx",
    ],
  },
  mode: "development",
  module: {
    ...common.module,
    rules: [
      ...common.module.rules,
    ],
  },
  output: {
    ...common.output,
    publicPath: "https://localhost:8401/static/",
  },
  plugins: [
    ...common.plugins,
    new webpack.HotModuleReplacementPlugin(),
  ],
};

const prod = {
  ...common,
  bail: true,
  mode: "production",
  module: {
    ...common.module,
    rules: [
      ...common.module.rules,
    ],
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: true,
          output: {
            comments: false,
            ecma: 5,
          },
          parse: {
            ecma: 9,
          },
        },
      }),
      new OptimizeCssAssetsPlugin(),
    ],
  },
  plugins: [
    ...common.plugins,
  ],
};

module.exports = {
  dev,
  prod,
}
