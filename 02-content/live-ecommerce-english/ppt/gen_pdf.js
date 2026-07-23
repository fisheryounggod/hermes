const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  const filePath = 'file://' + path.resolve('index.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for WebGL to initialize
  await page.waitForTimeout(2000);

  const slides = await page.$$('.slide');
  console.log('Total slides found:', slides.length);

  const pdfPaths = [];

  for (let i = 0; i < slides.length; i++) {
    await page.evaluate((idx) => {
      // Programmatically go to slide i
      const deck = document.getElementById('deck');
      deck.style.transform = `translateX(${-idx * 100}vw)`;
      // Update nav dots
      document.querySelectorAll('#nav .dot').forEach((d, j) => {
        d.classList.toggle('active', j === idx);
      });
    }, i);

    await page.waitForTimeout(1000);

    const pdf = await page.pdf({
      path: `slide_${String(i+1).padStart(2,'0')}.pdf`,
      width: '1920px',
      height: '1080px',
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });
    pdfPaths.push(pdf);
    console.log(`Slide ${i+1} done`);
  }

  await browser.close();
  console.log('All done');
})();
