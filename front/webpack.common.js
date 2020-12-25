const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const common = {
  entry: {
    cachipfs: './src/entrypoints/cachipfs.jsx',
    docs: './src/entrypoints/docs.jsx',
    index: './src/entrypoints/index.jsx',
    nixdb: './src/entrypoints/nixdb.jsx',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheCompression: false,
            cacheDirectory: true,
            plugins: [
              ['@babel/transform-runtime'],
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
        test: /\.(gif|jpe?g|png|svg)$/,
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
      {
        test: /\.md$/,
        use: [
          {
            loader: 'raw-loader',
            options: {
              esModule: false,
            },
          },
        ],
      },
    ],
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '../public/front'),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
    new webpack.ProvidePlugin({
      process: 'process/browser',
    }),
  ],
  resolve: {
    extensions: ['.js', '.jsx'],
    fallback: {
      'path': require.resolve('path-browserify'),
    },
  },
  stats: {
    children: true,
    colors: true,
    modules: true,
  },
};

const dev = {
  ...common,
  devtool: 'eval',
  entry: {
    cachipfs: [
      'webpack-dev-server/client?https://localhost:8401',
      'webpack/hot/only-dev-server',
      './src/entrypoints/cachipfs.jsx',
    ],
    docs: [
      'webpack-dev-server/client?https://localhost:8401',
      'webpack/hot/only-dev-server',
      './src/entrypoints/docs.jsx',
    ],
    index: [
      'webpack-dev-server/client?https://localhost:8401',
      'webpack/hot/only-dev-server',
      './src/entrypoints/index.jsx',
    ],
    nixdb: [
      'webpack-dev-server/client?https://localhost:8401',
      'webpack/hot/only-dev-server',
      './src/entrypoints/nixdb.jsx',
    ],
  },
  mode: 'development',
  module: {
    ...common.module,
    rules: [
      ...common.module.rules,
    ],
  },
  output: {
    ...common.output,
    publicPath: 'https://localhost:8401/front/',
  },
  plugins: [
    ...common.plugins,
    new webpack.HotModuleReplacementPlugin(),
  ],
};

const prod = {
  ...common,
  bail: true,
  mode: 'production',
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
