module.exports = {
  outputDir: "../librehq/templates",
  // assetsDir is relative to outputDir
  assetsDir: "../static/generated",
  pages: {
    signin: {
      entry: "src/pages/signin/main.js",
      template: "public/index.html",
      filename: "signin.html",
      title: "LibreHQ beta"
    },
    dashboard: {
      entry: "src/pages/dashboard/main.js",
      template: "public/index.html",
      filename: "dashboard.html",
      title: "Dashboard | LibreHQ beta"
    },
    account: {
      entry: "src/pages/account/main.js",
      template: "public/index.html",
      filename: "account.html",
      title: "My Account | LibreHQ beta"
    }
  }
};
