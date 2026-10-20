import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.BASE_URL || "http://127.0.0.1:4176";

export default defineConfig({
  testDir: "tests",
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  workers: 3,
  timeout: 600000,
  reporter: [["list"]],
  use: {
    baseURL,
    headless: true,
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
  webServer: {
    command: "python3 src/build.py && python3 -m http.server 4176 -d out --bind 127.0.0.1",
    url: baseURL,
    reuseExistingServer: true,
    timeout: 60000,
  },
});
