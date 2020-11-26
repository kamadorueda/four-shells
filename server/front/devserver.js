const WebpackDevServer = require('webpack-dev-server');
const devConfig = require('./webpack.common').dev;
const webpack = require('webpack');

const HOST = "localhost";
const PORT = 8401;

process.on(
  "unhandledRejection",
  (reason, promise) => {
    console.error("Unhandled Rejection at:", promise, "reason:", reason);
  }
);

const compiler = webpack(devConfig);
const serverConfig = {
  compress: true,
  /*
   * Access-Control-Allow-Origin response header tell the browser that the
   * content on this page is accessible from all origins.
   */
  // eslint-disable-next-line @typescript-eslint/naming-convention
  headers: { "Access-Control-Allow-Origin": "*" },
  historyApiFallback: true,
  hot: true,
  https: true,
  publicPath: devConfig.output.publicPath,
  sockHost: HOST,
  sockPort: PORT,
  stats: devConfig.stats,
  watchContentBase: true,
};

const devServer = new WebpackDevServer(
  compiler,
  serverConfig
);

devServer.listen(PORT, HOST, (serverError) => {
  if (serverError !== undefined) {
    console.log(serverError);
  }

  console.log("Starting the development server...\n");
});

(["SIGINT", "SIGTERM"]).forEach(
  (sig) => {
    process.on(sig, () => {
      devServer.close();
      process.exit();
    });
  }
);
