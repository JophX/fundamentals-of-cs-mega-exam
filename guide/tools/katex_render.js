// Reads a JSON array of {tex, display} on stdin, writes a JSON array of HTML strings.
const katex = require('katex');
let input = '';
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  const items = JSON.parse(input);
  const out = items.map(({ tex, display }) => {
    try {
      return katex.renderToString(tex, {
        displayMode: display,
        throwOnError: true,
        strict: 'ignore',
        macros: {
          '\\eps': '\\varepsilon',
          '\\lam': '\\lambda',
          '\\N': '\\mathbb{N}',
          '\\blank': '\\square',
          '\\ra': '\\rightarrow',
          '\\Ra': '\\Rightarrow',
        },
      });
    } catch (e) {
      return { error: String(e.message), tex };
    }
  });
  process.stdout.write(JSON.stringify(out));
});
