const path = require("path");
const fs = require("fs");
const { pathToFileURL } = require("url");
const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const frameworkRoot = path.resolve(__dirname, "../..");
const templatePath = path.join(frameworkRoot, "templates", "artifact.html");
const examplePaths = fs.readdirSync(path.join(frameworkRoot, "examples")).filter(name => name.endsWith(".html")).map(name => path.join(frameworkRoot, "examples", name));
const asUrl = filePath => pathToFileURL(filePath).href;

test("Core runtime creates the standard action Response", async ({ page }) => {
  const remote = [];
  page.on("request", request => { if (/^https?:/i.test(request.url())) remote.push(request.url()); });
  await page.goto(asUrl(templatePath));
  await page.locator('[data-response-selection][value="single-file"]').check();
  await page.locator("[data-response-comment]").fill("단일 전달 단위를 선택합니다.");
  await page.getByRole("button", { name: "Response 생성" }).click();
  const payload = JSON.parse(await page.locator("#response-output").textContent());
  expect(payload.spec).toBe("human-review-artifacts/review-response@0.2");
  expect(payload.artifact).toEqual({id:"artifact:template:core-0.3",spec:"human-review-artifacts/core@0.3",revision:"r1"});
  expect(payload.interaction.pattern).toEqual({name:"decide",version:"0.1"});
  expect(payload.responses).toEqual([{targetId:"decision-target",action:"select",selectionIds:["single-file"],comment:"단일 전달 단위를 선택합니다."}]);
  expect(remote).toEqual([]);
});

test("Core runtime prevents invalid select and comment actions", async ({ page }) => {
  await page.goto(asUrl(templatePath));
  await page.getByRole("button", { name: "Response 생성" }).click();
  await expect(page.locator("#response-error")).toContainText("선택이 필요");
  await page.locator("[data-response-action]").selectOption("request-changes");
  await page.getByRole("button", { name: "Response 생성" }).click();
  await expect(page.locator("#response-error")).toContainText("의견이 필요");
});

test("Response download is local and revisioned", async ({ page }) => {
  await page.goto(asUrl(templatePath));
  await page.locator('[data-response-selection][value="split-bundle"]').check();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "다운로드" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("artifact-template-core-0.3-r1-response.json");
});

test("Core content and interaction remain readable without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({javaScriptEnabled:false,locale:"ko-KR"});
  const page = await context.newPage(); await page.goto(asUrl(templatePath));
  for (const section of ["summary","content","interaction","provenance"]) await expect(page.locator(`[data-artifact-section="${section}"]`)).toBeVisible();
  await expect(page.locator('[data-manifest-field="revision"]')).toHaveText("r1");
  await context.close();
});

test("print and mobile views keep the requested action visible", async ({ page }) => {
  await page.goto(asUrl(templatePath)); await page.emulateMedia({media:"print"});
  await expect(page.locator('[data-artifact-section="interaction"]')).toBeVisible();
  await expect(page.locator('[data-artifact-section="provenance"]')).toBeVisible();
  await page.setViewportSize({width:390,height:844});
  await expect(page.locator("#decision-target")).toBeVisible();
});

test("reference Artifact has no automatically detectable accessibility violations", async ({ browser }) => {
  const context = await browser.newContext({bypassCSP:true,locale:"ko-KR"});
  const page = await context.newPage(); await page.goto(asUrl(templatePath));
  expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
  await context.close();
});

for (const examplePath of examplePaths) {
  test(`${path.basename(examplePath)} is a static readable Snapshot`, async ({ page }) => {
    const errors=[]; const remote=[];
    page.on("pageerror", error => errors.push(error.message));
    page.on("request", request => { if (/^https?:/i.test(request.url())) remote.push(request.url()); });
    await page.goto(asUrl(examplePath));
    await expect(page.locator("main[data-artifact-root]")).toBeVisible();
    await expect(page.locator('[data-artifact-section="interaction"]')).toBeVisible();
    await expect(page.locator("script[data-artifact-runtime]")).toHaveCount(0);
    expect(errors).toEqual([]); expect(remote).toEqual([]);
  });
}
