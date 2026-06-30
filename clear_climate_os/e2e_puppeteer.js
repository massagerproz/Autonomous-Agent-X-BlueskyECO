const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  // Give the server a moment to start if run in parallel
  console.log('Navigating to Streamlit app...');

  try {
    // Navigate to Streamlit's default port 8501
    await page.goto('http://localhost:8501', { waitUntil: 'networkidle0', timeout: 30000 });

    const title = await page.title();
    console.log(`Page title: ${title}`);

    if (!title.includes('CLEAR Climate')) {
      throw new Error('Title does not match expected "CLEAR Climate".');
    }

    // Wait for the main title to appear (Streamlit headers can be multiple h1 elements, so let's get all)
    await page.waitForSelector('h1', { timeout: 15000 });
    const h1Elements = await page.$$eval('h1', els => els.map(el => el.innerText));
    console.log(`H1 texts found: ${h1Elements.join(', ')}`);

    if (!h1Elements.some(text => text.includes('CLEAR Climate Copilot'))) {
      throw new Error('Main heading does not match expected.');
    }

    console.log('Puppeteer E2E test passed!');
  } catch (err) {
    console.error('Puppeteer E2E test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
