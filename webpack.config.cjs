const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports={
    mode: "production",
    performance: {
        hints: false,
        maxEntrypointSize: 512000,
        maxAssetSize: 512000
    },
    entry: ['@babel/polyfill','./src/index.js'],
    output:{
        filename: 'index.js',
        path: path.resolve(__dirname, 'static')
    }, 
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        rules: [
            {
                test: /\.js$|jsx/,
                include: [
                    path.resolve(__dirname, 'src')
                  ],
                use: ['babel-loader'],
            },
            
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            hash: true,
            filename: './templates/index.html' //relative to root of the application
        })
   ]
}