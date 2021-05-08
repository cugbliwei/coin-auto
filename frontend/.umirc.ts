import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  "proxy": {
    "/crawl": {
      "target": "http://localhost:8080",
      "changeOrigin": true,
    }
  },
  routes: [
    { path: '/', component: '@/pages/index' },
  ],
  copy: [
    'favicon.ico'
  ]
});
