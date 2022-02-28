export default {
  target: 'static',
  router: {
    base: '/api_documentation'
  },
  buildModules: ['@nuxtjs/tailwindcss'],
  head: {
    title: "[Alpha] ORP API Documentation",
    link: [
      { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Oxygen:wght@400;700&display=swap",
      },
    ],
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },

      // hid is used as unique identifier. Do not use `vmid` for it as it will not work
      { hid: 'description', name: 'description', content: 'Meta description' }
    ]
  },
}