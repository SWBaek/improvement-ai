const path = require("path");
const { pathToFileURL } = require("url");
const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const frameworkRoot = path.resolve(__dirname, "../..");
const templatePath = path.join(frameworkRoot, "templates", "artifact.html");
const decisionPath = path.join(frameworkRoot, "examples", "decision-review.html");
const researchPath = path.join(frameworkRoot, "examples", "research-review.html");
const examplePaths = [decisionPath, researchPath];
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
  for (const content of await page.locator(".section-content").all()) await expect(content).toBeHidden();
  await page.getByRole("button", { name: "모두 펼치기" }).click();
  await expect(page.locator('[data-artifact-section="summary"] .section-content')).toBeVisible();
  expect(remoteRequests).toEqual([]);
});

test("review target exports the standard Response envelope and downloads locally", async ({ page }) => {
  await page.goto(asUrl(templatePath));
  await page.getByRole("button", { name: "JSON 만들기" }).click();
  await expect(page.locator("#review-output")).toHaveValue("");
  await expect(page.locator("#export-status")).toContainText("필요한 선택 또는 의견");
  await page.locator("[data-review-disposition]").selectOption("selected");
  await page.locator("[data-review-option]").first().check();
  await page.locator("[data-review-comment]").fill("근거 링크를 추가합니다.");
  await page.getByRole("button", { name: "JSON 만들기" }).click();
  const payload = JSON.parse(await page.locator("#review-output").inputValue());
  expect(payload.spec).toBe("human-review-artifacts/review-response@0.1");
  expect(payload.artifact).toEqual({
    id: "artifact:template:core-0.2",
    spec: "human-review-artifacts/core@0.2",
    revision: "r1"
  });
  expect(payload.responses).toEqual([{
    targetId: "review-core",
    disposition: "selected",
    selectionIds: ["clarify-evidence"],
    comment: "근거 링크를 추가합니다."
  }]);
  expect(new Date(payload.createdAt).toString()).not.toBe("Invalid Date");
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "결과 다운로드" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("artifact-template-core-0.2-r1-review.json");
});

test("core content and review request remain readable without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(asUrl(templatePath));
  for (const section of ["summary", "content", "review-request", "provenance"]) {
    await expect(page.locator(`[data-artifact-section="${section}"]`)).toBeVisible();
  }
  await expect(page.locator('[data-manifest-field="revision"]')).toHaveText("r1");
  await context.close();
});

test("print view keeps review content and provenance visible", async ({ page }) => {
  await page.goto(asUrl(templatePath));
  await page.emulateMedia({ media: "print" });
  await expect(page.locator('[data-artifact-section="review-request"]')).toBeVisible();
  await expect(page.locator('[data-artifact-section="provenance"]')).toBeVisible();
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
  test(`${path.basename(examplePath)} renders without runtime errors or remote requests`, async ({ page }) => {
    const errors = [];
    const remoteRequests = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("request", (request) => {
      if (/^https?:/i.test(request.url())) remoteRequests.push(request.url());
    });
    await page.goto(asUrl(examplePath));
    await expect(page.locator("main[data-artifact-root]")).toBeVisible();
    await expect(page.locator('[data-manifest-field="revision"]')).toHaveText("r1");
    expect(errors).toEqual([]);
    expect(remoteRequests).toEqual([]);
  });
}

test("research example is a static generated Snapshot with input provenance", async ({ page }) => {
  await page.goto(asUrl(researchPath));
  await expect(page.locator("script[data-artifact-runtime]")).toHaveCount(0);
  await expect(page.locator('[data-artifact-section="review-request"]')).toHaveCount(0);
  await expect(page.locator('[data-artifact-section="provenance"]')).toBeVisible();
});
