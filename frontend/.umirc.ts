import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  "proxy": {
    "/coin": {
      "target": "http://localhost:7998",
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
