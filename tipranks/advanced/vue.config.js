module.exports = {
    outputDir: './dist',
     devServer: { 
         proxy: { 
             '/api': { target: 'https://www.tipranks.com', changeOrigin: true, ws: true, pathRewrite: { '^/api':  '/api', } } 
            }
    }
  }