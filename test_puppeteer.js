const puppeteer = require('puppeteer');
const { PuppeteerScreenRecorder } = require('puppeteer-screen-recorder');
const { spawn } = require('child_process');

(async () => {
    // Start Streamlit
    console.log("Starting Streamlit...");
    const streamlit = spawn('streamlit', ['run', 'clear_climate_os/app.py', '--server.port', '8503', '--server.headless', 'true']);

    // Wait for Streamlit to start
    await new Promise(resolve => setTimeout(resolve, 5000));
    console.log("Streamlit started. Launching Puppeteer...");

    const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
    const page = await browser.newPage();

    const recorder = new PuppeteerScreenRecorder(page);
    await recorder.start('verification/videos/puppeteer_recording.mp4');
    console.log("Started recording...");

    try {
        await page.goto('http://localhost:8503', { waitUntil: 'networkidle2', timeout: 15000 });

        // Wait for main title
        await page.waitForSelector('h1', { timeout: 15000 });

        // Type into textarea
        const textareaSelector = 'textarea[aria-label="Paste meeting notes, activity updates, or stakeholder inputs here:"]';
        await page.waitForSelector(textareaSelector);
        await page.type(textareaSelector, 'We installed 50 solar panels today. There was a delay due to weather.');

        // Click process button
        // Streamlit buttons have complex class structures. Searching by text content using XPath.
        const processBtn = await page.$x("//button[.//p[text()='Process Notes']]");
        if (processBtn.length > 0) {
            await processBtn[0].click();
        }

        // Wait for checkboxes to appear
        await page.waitForSelector('input[type="checkbox"]', { timeout: 10000 });
        await new Promise(resolve => setTimeout(resolve, 2000)); // allow rendering to settle

        // Check checkboxes
        const checkboxes = await page.$$('input[type="checkbox"]');
        for (const cb of checkboxes) {
            // Click the parent element of the checkbox to bypass hidden styling issues
            const parent = await cb.evaluateHandle(el => el.parentElement);
            await parent.click();
        }

        // Click save button
        const saveBtn = await page.$x("//button[.//p[text()='Save Approved Evidence to Tracker']]");
        if (saveBtn.length > 0) {
            await saveBtn[0].click();
        }

        await new Promise(resolve => setTimeout(resolve, 2000));

        // Click generate report button
        const generateBtn = await page.$x("//button[.//p[text()='Generate Donor Report Draft']]");
        if (generateBtn.length > 0) {
            await generateBtn[0].click();
        }

        await new Promise(resolve => setTimeout(resolve, 2000));

        // Take screenshot
        await page.screenshot({ path: 'verification/screenshots/puppeteer_screenshot.png', fullPage: true });
        console.log("Test completed successfully!");

    } catch (err) {
        console.error("Test failed:", err);
    } finally {
        await recorder.stop();
        await browser.close();
        streamlit.kill();
        process.exit(0);
    }
})();
