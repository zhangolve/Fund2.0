module.exports = {
    outputDir: './dist',
     devServer: { 
         proxy: { 
             '/api': { target: 'https://www.tipranks.com', changeOrigin: true, ws: true, pathRewrite: { '^/api':  '/api', } } 
            }
    },
    chainWebpack: config => {
        config
        .plugin('html')
        .tap(args => {
          args[0].title = 'tipranks details'
          return args
        })
      }
  }