module.exports = {
  server: {
    port: 8000,       // default: 3000
    host: '0.0.0.0',  // default: localhost
  },
  head: {
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    ],
    link: [
      { rel: 'stylesheet', href: '/styles/github.css' },
      { rel: 'stylesheet', href: '/styles/index.css' },
      { rel: 'stylesheet', href: '/styles/detail.css' },
      { rel: 'stylesheet', href: '/styles/iview-3.4.1.css' },
    ]
  },
  env: {
    // 好像没起作用？
    NODE_ENV: process.env.NODE_ENV || 'development'
  },
  build: {
    vendor: ['axios', 'iview']
  },
  plugins: [
    { src: '~/plugins/iview.js', ssr: true }
    // { src: '~/plugins/iview.js', mode: "server"}
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/proxy'
  ],
  proxy: {
    '/api': {
      target: 'http://server_py:8010',
      changeOrigin: true,
      // pathRewrite: {
      //   '^/api': '/',
      // }
    },
  }
}
