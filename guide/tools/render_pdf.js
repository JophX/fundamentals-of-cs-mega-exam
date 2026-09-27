// Usage: node render_pdf.js <input.html> <output.pdf>
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

(async () => {
  const [inFile, outFile] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inFile), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: outFile,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="font-size:8px;width:100%;text-align:center;color:#888;font-family:sans-serif">' +
      'Mega Study Guide — 5DV037 &amp; 5DV086 &nbsp;·&nbsp; page <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '16mm', left: '15mm', right: '15mm' },
  });
  await browser.close();
})();
