const GitRevisionPlugin = require('git-revision-webpack-plugin');

const gitRevisionPlugin = new GitRevisionPlugin({
	versionCommand: 'describe --always --tags',
});

process.env.VUE_APP_VERSION = gitRevisionPlugin.version();

module.exports = {
	chainWebpack: config => {
		config.module
			.rule('csv')
			.test(/\.csv$/)
			.use('raw-loader')
			.loader('raw-loader')
			.end()
	},
}
