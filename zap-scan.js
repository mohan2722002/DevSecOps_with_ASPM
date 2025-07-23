const ZapClient = require('zaproxy');
const fs = require('fs');

const zap = new ZapClient({
  apiKey: 'changeme',
  proxy: { host: '127.0.0.1', port: 9090 } // matches exposed ZAP daemon
});

(async () => {
  const target = 'http://www:80'; // container name in Docker network
  console.log(`🕷️ Starting scan on: ${target}`);

  const { scan } = await zap.spider.scan({ url: target });

  let status = '0';
  while (status !== '100') {
    await new Promise(r => setTimeout(r, 3000));
    status = (await zap.spider.status({ scanId: scan })).status;
    console.log(`🔍 Spider progress: ${status}%`);
  }

  const alerts = await zap.core.alerts({ baseurl: target });
  fs.writeFileSync('zap_alerts.json', JSON.stringify(alerts, null, 2));
  console.log(`✅ Scan finished: ${alerts.length} alerts written to zap_alerts.json`);
})();
