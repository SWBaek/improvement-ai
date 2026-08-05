const path = require("path");
const { pathToFileURL } = require("url");
const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const frameworkRoot = path.resolve(__dirname, "../..");
const templatePath = path.join(frameworkRoot, "templates", "artifact.html");
const examplePaths = [
  path.join(frameworkRoot, "examples", "decision-review.html"),
  path.join(frameworkRoot, "examples", "research-review.html")
];

const asUrl = (filePath) => pathToFileURL(filePath).href;

test("reference Artifact supports navigation, filtering and collapsing", async ({ page }) => {
  const remoteRequests = [];
  page.on("request", (request) => {
    if (/^https?:/i.test(request.url())) remoteRequests.push(request.url());
  });

  await page.goto(asUrl(templatePath));
  await expect(page.locator("h1")).toHaveText("Human Review Artifact");
  await expect(page.locator("#artifact-nav-list a")).toHaveCount(4);

  await page.getByRole("button", { name: "가정" }).click();
  await expect(page.locator('[data-artifact-kind="assumption"]')).toBeVisible();
  await expect(page.locator('[data-artifact-kind="fact"]')).toBeHidden();

  await page.getByRole("button", { name: "전체" }).click();
  await page.getByRole("button", { name: "모두 접기" }).click();
  await expect(page.locator(".section-content")).toHaveCount(4);
  for (const content of await page.locator(".section-content").all()) {
    await expect(content).toBeHidden();
  }

  await page.getByRole("button", { name: "모두 펼치기" }).click();
  await expect(page.locator('[data-artifact-section="summary"] .section-content')).toBeVisible();
  expect(remoteRequests).toEqual([]);
});

test("review choices export as JSON and download locally", async ({ page }) => {
  await page.goto(asUrl(templatePath));
  await page.locator("[data-review-option]").first().check();
  await page.locator("#review-note").fill("근거 링크를 추가합니다.");
  await page.getByRole("button", { name: "JSON 만들기" }).click();

  const output = await page.locator("#review-output").inputValue();
  const payload = JSON.parse(output);
  expect(payload.artifactId).toBe("artifact:template:core-0.1");
  expect(payload.selections).toEqual(["clarify-evidence"]);
  expect(payload.note).toBe("근거 링크를 추가합니다.");

  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "결과 다운로드" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("artifact-template-core-0.1-review.json");
});

test("core content remains readable without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(asUrl(templatePath));

  await expect(page.locator('[data-artifact-section="summary"]')).toBeVisible();
  await expect(page.locator('[data-artifact-section="content"]')).toBeVisible();
  await expect(page.locator('[data-artifact-section="review-request"]')).toBeVisible();
  await expect(page.locator('[data-artifact-section="provenance"]')).toBeVisible();
  await context.close();
});

test("reference Artifact has no automatically detectable accessibility violations", async ({ browser }) => {
  const context = await browser.newContext({ bypassCSP: true, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(asUrl(templatePath));
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
  await context.close();
});

for (const examplePath of examplePaths) {
  test(`${path.basename(examplePath)} renders without runtime errors`, async ({ page }) => {
    const errors = [];
    const remoteRequests = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("request", (request) => {
      if (/^https?:/i.test(request.url())) remoteRequests.push(request.url());
    });
    await page.goto(asUrl(examplePath));
    await expect(page.locator("main[data-artifact-root]")).toBeVisible();
    await expect(page.locator("#review-output")).not.toHaveValue("");
    expect(errors).toEqual([]);
    expect(remoteRequests).toEqual([]);
  });
}
