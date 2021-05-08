import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  "proxy": {
    "/api": {
      "target": "http://localhost:3389",
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
