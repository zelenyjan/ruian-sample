import { createApp } from "vue";
import { createPinia } from "pinia";
import RuianSampleApp from "src/RuianSampleApp.vue";

document.addEventListener(
  "DOMContentLoaded",
  () => {
    if (document.getElementById("app")) {
      const pinia = createPinia();
      const app = createApp(RuianSampleApp);
      // storage
      app.use(pinia);
      app.mount("#app");
    }
  },
  false,
);
