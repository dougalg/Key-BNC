module.exports = {
	chainWebpack: config => {
		config.module
			.rule('csv')
			.test(/\.csv$/)
			.use('raw-loader')
				.loader('raw-loader')
				.end()
	}
}
