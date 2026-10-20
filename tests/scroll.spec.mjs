import { test, expect } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

const PAGES = [
  "/",
  "/about/",
  "/coverage/",
  "/client-center/",
  "/contact/",
  "/legal/",
  "/policy-review/",
  "/404.html",
  "/coverage/real-estate/",
  "/coverage/hospitality/",
  "/coverage/construction/",
  "/coverage/professional/",
  "/coverage/personal/",
  "/checklists/",
  "/needs/",
  "/quote/",
  "/resources/",
  "/partners/",
  "/switching/",
  "/photo-credits/",
  "/style-preview/",
  "/new-york-building-insurance/",
  "/new-york-contractor-insurance/",
  "/new-york-restaurant-insurance/",
];

const DESKTOP = [
  { width: 1440, height: 900 },
  { width: 1280, height: 800 },
];

function reportPath(name) {
  const dir = process.env.SCROLL_REPORT_DIR || "test-results";
  fs.mkdirSync(dir, { recursive: true });
  return path.join(dir, `scroll-${name}.json`);
}

async function metrics(page) {
  return page.evaluate(() => {
    const max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const footer = document.querySelector("footer.site-footer");
    const fr = footer ? footer.getBoundingClientRect() : null;
    const ports = [];
    document.querySelectorAll("body *").forEach((el) => {
      const cs = getComputedStyle(el);
      const oy = cs.overflowY;
      const ox = cs.overflowX;
      const scrollable = ["hidden", "auto", "scroll"].includes(oy) || ["hidden", "auto", "scroll"].includes(ox);
      if (!scrollable) return;
      const extraY = el.scrollHeight - el.clientHeight;
      const extraX = el.scrollWidth - el.clientWidth;
      if (extraY < 8 && extraX < 8) return;
      const r = el.getBoundingClientRect();
      if (r.width < 160 || r.height < 160) return;
      ports.push(
        (el.className && String(el.className).trim().slice(0, 48)) || el.tagName
      );
    });
    return {
      y: window.scrollY,
      max,
      doc: document.documentElement.scrollHeight,
      inner: window.innerHeight,
      htmlOverflow: getComputedStyle(document.documentElement).overflowY,
      bodyOverflow: getComputedStyle(document.body).overflowY,
      bodyPosition: getComputedStyle(document.body).position,
      navOpen: document.documentElement.classList.contains("nav-open"),
      blocks: window.__scrollBlocks || [],
      ports: [...new Set(ports)].slice(0, 8),
      footerTop: fr ? Math.round(fr.top) : null,
      footerBottom: fr ? Math.round(fr.bottom) : null,
      hasFooter: !!footer,
    };
  });
}

async function resetTop(page) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(120);
}

async function waitMoved(page, startY, minMs = 400) {
  await page.evaluate(
    async ({ start, minMs }) => {
      const t0 = performance.now();
      let last = window.scrollY;
      let lastChange = t0;
      while (performance.now() - t0 < 1100) {
        await new Promise((resolve) => setTimeout(resolve, 40));
        const y = window.scrollY;
        const now = performance.now();
        if (y !== last) {
          last = y;
          lastChange = now;
        }
        if (now - t0 >= minMs && y !== start && now - lastChange >= 80) return;
      }
    },
    { start: startY, minMs }
  );
}

async function focusPage(page) {
  await page.evaluate(() => {
    const active = document.activeElement;
    if (active && active !== document.body && active.blur) active.blur();
    document.body.tabIndex = -1;
    document.body.focus();
  });
}

async function wheelAt(page, delta, minMs = 400) {
  const point = await page.evaluate(() => {
    const spots = [
      [Math.round(innerWidth * 0.72), Math.round(innerHeight * 0.62)],
      [Math.round(innerWidth * 0.28), Math.round(innerHeight * 0.45)],
      [Math.round(innerWidth * 0.5), Math.round(innerHeight * 0.78)],
    ];
    for (const [x, y] of spots) {
      const el = document.elementFromPoint(x, y);
      if (!el || el.tagName === "IFRAME") continue;
      if (el.closest && el.closest("iframe")) continue;
      return { x, y };
    }
    return { x: 48, y: Math.round(innerHeight * 0.7) };
  });
  const startY = await page.evaluate(() => window.scrollY);
  await page.mouse.move(point.x, point.y);
  await page.mouse.wheel(0, delta);
  await waitMoved(page, startY, minMs);
}

test.beforeEach(async ({ context }) => {
  await context.addInitScript(() => {
    const orig = EventTarget.prototype.addEventListener;
    window.__scrollBlocks = [];
    EventTarget.prototype.addEventListener = function (type, fn, opts) {
      let passive = true;
      if (opts && typeof opts === "object" && opts.passive === false) passive = false;
      if ((type === "wheel" || type === "mousewheel" || type === "touchmove") && !passive) {
        window.__scrollBlocks.push(type);
      }
      return orig.call(this, type, fn, opts);
    };
  });
});

test("desktop wheel, trackpad, and keyboard scroll every page", async ({ page, browserName }, testInfo) => {
  const rows = [];
  try {
  for (const viewport of DESKTOP) {
    await page.setViewportSize(viewport);
    for (const href of PAGES) {
      const row = { browser: browserName, viewport: `${viewport.width}x${viewport.height}`, page: href };
      await page.goto(href, { waitUntil: "domcontentloaded" });
      await page.waitForTimeout(120);
      await resetTop(page);
      const start = await metrics(page);
      row.scrollable = start.max > 40;
      row.navOpen = start.navOpen;
      row.bodyPosition = start.bodyPosition;
      row.blocks = start.blocks;
      row.ports = start.ports;

      if (!row.scrollable) {
        row.wheel100 = "n/a";
        row.wheel800 = "n/a";
        row.trackpad = "n/a";
        row.pageDown = "n/a";
        row.space = "n/a";
        row.footer = start.hasFooter ? "short" : "no-footer";
        rows.push(row);
        expect.soft(start.navOpen, href).toBe(false);
        expect.soft(start.bodyPosition, href).toBe("static");
        expect.soft(start.blocks, href).toEqual([]);
        continue;
      }

      await wheelAt(page, 100);
      const after100 = await metrics(page);
      row.wheel100 = after100.y - start.y;

      await resetTop(page);
      const before800 = await metrics(page);
      await wheelAt(page, 800);
      const after800 = await metrics(page);
      row.wheel800 = after800.y - before800.y;

      await resetTop(page);
      const beforePad = await metrics(page);
      for (const delta of [8, 12, 16, 24]) await wheelAt(page, delta);
      const afterPad = await metrics(page);
      row.trackpad = afterPad.y - beforePad.y;

      await resetTop(page);
      await focusPage(page);
      const beforeKey = await metrics(page);
      await page.keyboard.press("PageDown");
      await waitMoved(page, beforeKey.y);
      const afterPd = await metrics(page);
      row.pageDown = afterPd.y - beforeKey.y;

      await resetTop(page);
      await focusPage(page);
      const beforeSpace = await metrics(page);
      await page.keyboard.press("Space");
      await waitMoved(page, beforeSpace.y);
      const afterSp = await metrics(page);
      row.space = afterSp.y - beforeSpace.y;

      await resetTop(page);
      for (let i = 0; i < 24; i++) {
        const now = await page.evaluate(() => ({
          y: window.scrollY,
          max: Math.max(0, document.documentElement.scrollHeight - window.innerHeight),
        }));
        if (now.y >= now.max - 2) break;
        await wheelAt(page, 800, 160);
      }
      const end = await metrics(page);
      row.reachedBottom = end.y >= end.max - 2;
      row.footerBottom = end.footerBottom;
      row.footerVisible = end.hasFooter && end.footerBottom !== null && end.footerBottom <= end.inner + 4 && end.footerTop < end.inner;

      const need800 = Math.min(400, start.max - 2);
      expect.soft(row.wheel100, `${href} wheel 100`).toBeGreaterThan(0);
      expect.soft(row.wheel800, `${href} wheel 800`).toBeGreaterThanOrEqual(need800);
      expect.soft(row.trackpad, `${href} trackpad`).toBeGreaterThan(0);
      expect.soft(row.pageDown, `${href} PageDown`).toBeGreaterThan(0);
      expect.soft(row.space, `${href} Space`).toBeGreaterThan(0);
      expect.soft(row.reachedBottom, `${href} bottom`).toBe(true);
      if (start.hasFooter) expect.soft(row.footerVisible, `${href} footer`).toBe(true);
      expect.soft(start.navOpen, href).toBe(false);
      expect.soft(start.bodyPosition, href).not.toBe("fixed");
      expect.soft(start.blocks, `${href} listeners`).toEqual([]);
      expect.soft(start.ports, `${href} scrollports`).toEqual([]);
      rows.push(row);
    }
  }
  } finally {
    fs.writeFileSync(reportPath(`${browserName}-${testInfo.project.name}`), JSON.stringify(rows, null, 2));
  }
});

test("touch swipe scrolls at 390x844", async ({ page, browserName }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const rows = [];
  for (const href of PAGES) {
    await page.goto(href, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(100);
    await resetTop(page);
    const start = await metrics(page);
    const row = {
      browser: browserName,
      viewport: "390x844",
      page: href,
      scrollable: start.max > 40,
      blocks: start.blocks,
      ports: start.ports,
    };
    if (!row.scrollable) {
      row.touch = "n/a";
      rows.push(row);
      continue;
    }
    if (browserName === "chromium") {
      const client = await page.context().newCDPSession(page);
      let y = 720;
      const x = 180;
      await client.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [{ x, y, id: 1 }],
      });
      for (let i = 0; i < 14; i++) {
        y -= 32;
        await client.send("Input.dispatchTouchEvent", {
          type: "touchMove",
          touchPoints: [{ x, y, id: 1 }],
        });
      }
      await client.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
      await page.waitForTimeout(80);
      const after = await metrics(page);
      row.touch = after.y - start.y;
      for (let i = 0; i < 12; i++) {
        const now = await metrics(page);
        if (now.y >= now.max - 2) break;
        let yy = 700;
        await client.send("Input.dispatchTouchEvent", {
          type: "touchStart",
          touchPoints: [{ x, y: yy, id: 1 }],
        });
        for (let s = 0; s < 10; s++) {
          yy -= 40;
          await client.send("Input.dispatchTouchEvent", {
            type: "touchMove",
            touchPoints: [{ x, y: yy, id: 1 }],
          });
        }
        await client.send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
        await page.waitForTimeout(30);
      }
      const end = await metrics(page);
      row.reachedBottom = end.y >= end.max - 2;
      row.footerVisible = end.hasFooter && end.footerBottom !== null && end.footerBottom <= end.inner + 4;
      expect.soft(row.touch, `${href} touch`).toBeGreaterThan(0);
      expect.soft(row.reachedBottom, `${href} touch bottom`).toBe(true);
      if (start.hasFooter) expect.soft(row.footerVisible, `${href} touch footer`).toBe(true);
    } else {
      const touchAction = await page.evaluate(() => getComputedStyle(document.body).touchAction);
      row.touchAction = touchAction;
      await wheelAt(page, 800);
      const after = await metrics(page);
      row.wheel800 = after.y - start.y;
      row.touch = "engine-cannot-pan";
      expect.soft(touchAction, href).toBe("auto");
      expect.soft(start.blocks, href).toEqual([]);
      expect.soft(row.wheel800, `${href} 390 wheel`).toBeGreaterThan(0);
    }
    expect.soft(start.ports, `${href} scrollports`).toEqual([]);
    rows.push(row);
  }
  fs.writeFileSync(reportPath(`${browserName}-touch`), JSON.stringify(rows, null, 2));
});
