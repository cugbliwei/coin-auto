import { defineConfig } from 'umi';

export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  "publicPath": "/static/",
  "proxy": {
    "/api": {
      "target": "http://localhost:3389",
      "changeOrigin": true,
    }
  },
  routes: [
    { path: '/coin/index', component: '@/pages/index' },
  ],
  copy: [
    'favicon.ico'
  ]
});
