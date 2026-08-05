const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./frameworks/human-review-artifacts/tests/browser",
  outputDir: "./test-results/human-review-artifacts",
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  use: {
    ...devices["Desktop Chrome"],
    locale: "ko-KR",
    trace: "retain-on-failure"
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" }
    }
  ]
});
