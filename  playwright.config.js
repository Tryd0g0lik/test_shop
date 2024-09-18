// playwright.config.js
import { defineConfig } from '@playwright/test';

export default defineConfig({
    use: {
        headless: true, // Run tests in headed mode
        viewport: { width: 1280, height: 720 }, // Set the viewport size
        ignoreHTTPSErrors: true, // Ignore HTTPS errors
    },
    projects: [
        {
            name: 'Chromium',
            use: { browserName: 'chromium' },
        },
        {
            name: 'Firefox',
            use: { browserName: 'firefox' },
        },
        {
            name: 'WebKit',
            use: { browserName: 'webkit' },
        },
    ],
});
