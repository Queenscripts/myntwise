import { resolve as _resolve } from 'path';
import HtmlWebpackPlugin from 'html-webpack-plugin';

export const mode = 'production';
export const entry = _resolve(__dirname, 'src/index.js');
export const output = {
    filename: 'index.js',
    path: _resolve(__dirname, 'static')
};
export const resolve = {
    extensions: ['', '.js', '.jsx']
};
export const module = {
    rules: [
        {
            test: /\.js$|jsx/,
            include: [
                _resolve(__dirname, 'src')
            ],
            use: ['babel-loader'],
        },
    ]
};
export const plugins = [
    new HtmlWebpackPlugin({
        hash: true,
        filename: './templates/index.html' //relative to root of the application
    })
];