const purgeCSS = require("@fullhuman/postcss-purgecss");
const postcssFontMagician = require("postcss-font-magician");
const cssNano = require("cssnano");

module.exports = (env) => {
  let plugins = [
    postcssFontMagician({
      hosted: ["static/src/ruian/fonts"],
      foundries: ["google"],
    }),
    "autoprefixer",
  ];

  if (env.mode === "production") {
    // purge css and mimify for production
    plugins = plugins.concat([
      cssNano({
        preset: "default",
      }),
    ]);
  }

  return {
    plugins: plugins,
  };
};
