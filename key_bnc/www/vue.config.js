/* eslint-disable indent */
const GitRevisionPlugin = require('git-revision-webpack-plugin')

const gitRevisionPlugin = new GitRevisionPlugin({
	versionCommand: 'describe --always --tags',
})

process.env.VUE_APP_VERSION = gitRevisionPlugin.version()

module.exports = {
	chainWebpack: config => {
		config.module
			.rule('csv')
				.test(/\.csv$/)
				.use('raw-loader')
				.loader('raw-loader')
				.end()
			.end()
			.rule('images')
				.exclude.add(/key-bnc-logo-225x278\.png$/)
				.end()
			.end()
			.rule('logo')
				.test(/key-bnc-logo(white)?-225x278\.png$/)
				.use('url-loader')
				.loader('url-loader')
			.end()
	},
}
